# This file is part of the Astrometry.net suite.
# Licensed under a 3-clause BSD style license - see LICENSE
from __future__ import print_function
from __future__ import absolute_import
import numpy as np
from astropy.wcs import WCS

class ResampleError(Exception):
    pass
class OverlapError(ResampleError):
    pass
class NoOverlapError(OverlapError):
    pass
class SmallOverlapError(OverlapError):
    pass

class WCSWrap():
    """ A thin layer for Astropy WCS object to function properly with the resampling code"""

    def __init__(self,w):
        self._wcs = w  # save astropy WCS object
    
    @property
    def imagew(self):
        return self._wcs.array_shape[1]

    @property
    def imageh(self):
        return self._wcs.array_shape[0]    
        
    def pixelxy2radec(self,x,y):
        # should use IRAF format
        ra,dec = self._wcs.all_pix2world(x,y,1)
        return ra,dec

    def radec2pixelxy(self,ra,dec):
        x,y = self._wcs.all_world2pix(ra,dec,1)
        ny,nx = self._wcs.array_shape
        ok = ((x>=0) & (x<=nx-1) & (y>=0) & (y<=ny-1))
        return ok,x,y
        

def resample_with_wcs(targetwcs, wcs, Limages=[], L=3, spline=True,
                      splineFallback=True,splineStep=25,splineMargin=12,
                      table=True,cinterp=True,intType=np.int32,oned=False):
    """
    Resample image with Lanczos using input and target WCS.

    When used with oned==True to return 1-D arrays

    target[Yo,Xo] = ims[i]

    raises NoOverlapError if the target and input WCSes do not
    overlap.  Raises SmallOverlapError if they do not overlap "enough"
    (as described below).

    targetwcs, wcs: duck-typed WCS objects that must have:
       - properties "imagew", "imageh"
       - methods  "r,d = pixelxy2radec(x, y)"
       -          "ok,x,y = radec2pixelxy(ra, dec)"

    The WCS functions are expected to operate in FITS pixel-indexing.

    The WCS function must support 1-d, broadcasting, vectorized
    pixel<->radec calls.

    Parameters
    ----------
    targetwcs : wcs object
       Target WCS object.  Can be astropy WCS object or any type
         that obeys the above duck-typing rules.
    wcs : wcs object
       Input WCS object.  Can be astropy WCS object or any type
         that obeys the above duck-typing rules.
    Limages : list
       List of input images to resample.
    L : int, optional
       Lanczos order (3 or 5).  Default is 3.
    spline : bool, optional
       Use a spline interpolator to reduce the number of WCS calls.
         Default is True.
    splineFallback : bool, optional
       The spline requires a certain amount of spatial overlap.  With
         splineFallback = True, fall back to non-spline version.
         With splineFallback = False, just raises SmallOverlapError.
         Default is True.
    splineStep : int, optional
       Step size for spline interpolation.  Default is 25.
    splineMargin : int, optional
       Side margins for spline interpolation.  Default is 12.
    table : bool, optional
       Use Lanczos look-up table.  Default is True.
    cinterp : bool, optional
       Use C extension for Lanczos interpolation. Default is True.
    intType : type, optional
       Type to return for integer pixel coordinates. Default is numpy.int32.
    oned : bool, optional
       Return 1-D arrays instead of 2-D images.  Default is False.

    Returns
    -------
    iyo : numpy array
       1-D array of Y-values for the resampled pixels in the output/target WCS.
          Only if oned==True.
    ixo : numpy array
       1-D array of X-values for the resampled pixels in the output/target WCS.
          Only if oned==True.
    iyi : numpy array
       1-D array of Y-values for the resampled pixels in the input WCS.
          Only if oned==True.
    ixi : numpy array
       1-D array of X-values for the resampled pixels in the input WCS.
          Only if oned==True.
    rims : numpy array
       List of the output resampled images.  If oned==True, then each element
         is 1-D array of values.  If oned==False, then they are full 2-D image
         arrays with non-overlapping pixels set to NaN.
         Default is oned==False.
    mask : numpy array
       Boolean mask of which output pixels are covered.  Only returned if
         oned==False.

    Example
    -------

    Return 2-D images

    ims,mask = resample_with_wcs(targetwcs,wcs,images)

    Return 1-D arrays

    iyo,ixo,iyi,ixi,rims = resample_with_wcs(targetwcs,wcs,images)


    """

    
    ### DEBUG
    #ps = PlotSequence('resample')
    ps = None

    # Make sure input Limages is a list or tuple
    listinput = True
    if type(Limages) is not list and type(Limages) is not tuple:
        Limages = [Limages]
        listinput = False
        
    # Astropy WCS input, wrap it
    if isinstance(targetwcs,WCS):
        targetwcs = WCSWrap(targetwcs)
    if isinstance(wcs,WCS):
        wcs = WCSWrap(wcs) 
        
    H,W = int(targetwcs.imageh), int(targetwcs.imagew)
    h,w = int(      wcs.imageh), int(      wcs.imagew)
    
    for im in Limages:
        assert(im.shape == (h,w))
    
    # First find the approximate bbox of the input image in
    # the target image so that we don't ask for way too
    # many out-of-bounds pixels...
    XY = []
    for x,y in [(0,0), (w-1,0), (w-1,h-1), (0, h-1)]:
        # [-2:]: handle ok,ra,dec or ra,dec
        ok,xw,yw = targetwcs.radec2pixelxy(
            *(wcs.pixelxy2radec(float(x + 1), float(y + 1))[-2:]))
        XY.append((xw - 1, yw - 1))
    XY = np.array(XY)

    x0,y0 = np.rint(XY.min(axis=0))
    x1,y1 = np.rint(XY.max(axis=0))
    
    if spline:
        # Now we build a spline that maps "target" pixels to "input" pixels
        margin = splineMargin
        step = splineStep
        xlo = max(0, x0-margin)
        xhi = min(W-1, x1+margin)
        ylo = max(0, y0-margin)
        yhi = min(H-1, y1+margin)
        if xlo > xhi or ylo > yhi:
            raise NoOverlapError()
        nx = int(np.ceil(float(xhi - xlo) / step)) + 1
        xx = np.linspace(xlo, xhi, nx)
        ny = int(np.ceil(float(yhi - ylo) / step)) + 1
        yy = np.linspace(ylo, yhi, ny)

        if ps:
            def expand_axes():
                M = 100
                ax = plt.axis()
                plt.axis([ax[0]-M, ax[1]+M, ax[2]-M, ax[3]+M])
                plt.axis('scaled')

                plt.clf()
            plt.plot(XY[:,0], XY[:,1], 'ro')
            plt.plot(xx, np.zeros_like(xx), 'b.')
            plt.plot(np.zeros_like(yy), yy, 'c.')
            plt.plot(xx, np.zeros_like(xx)+max(yy), 'b.')
            plt.plot(max(xx) + np.zeros_like(yy), yy, 'c.')
            plt.plot([0,W,W,0,0], [0,0,H,H,0], 'k-')
            plt.title('A: Target image: bbox')
            expand_axes()
            ps.savefig()

        if (len(xx) == 0) or (len(yy) == 0):
            raise NoOverlapError()

        if (len(xx) <= 3) or (len(yy) <= 3):
            #print 'Not enough overlap between input and target WCSes'
            if splineFallback:
                spline = False
            else:
                raise SmallOverlapError()
            
    if spline:
        # spline inputs  -- pixel coords in the 'target' image
        #    (xx, yy)
        # spline outputs -- pixel coords in the 'input' image
        #    (XX, YY)
        # We use vectorized radec <-> pixelxy functions here

        R = targetwcs.pixelxy2radec(xx[np.newaxis,:] + 1,
                                    yy[:,np.newaxis] + 1)
        if len(R) == 3:
            ok = R[0]
            assert(np.all(ok))
        ok,XX,YY = wcs.radec2pixelxy(*(R[-2:]))        
        del R
        XX -= 1.
        YY -= 1.
        #assert(np.all(ok))  # now sure what this is checking for exactly
        del ok
        
        if ps:
            plt.clf()
            plt.plot(Xo, Yo, 'b.')
            plt.plot([0,w,w,0,0], [0,0,h,h,0], 'k-')
            plt.title('B: Input image')
            expand_axes()
            ps.savefig()
    
        import scipy.interpolate as interp
        xspline = interp.RectBivariateSpline(xx, yy, XX.T)
        yspline = interp.RectBivariateSpline(xx, yy, YY.T)
        del XX
        del YY

    else:
        margin = 0

    # Now, build the full pixel grid (in the ouput image) we want to
    # interpolate...
    ixo = np.arange(max(0, x0-margin), min(W, x1+margin+1), dtype=intType)
    iyo = np.arange(max(0, y0-margin), min(H, y1+margin+1), dtype=intType)

    if len(ixo) == 0 or len(iyo) == 0:
        raise NoOverlapError()

    if spline:
        # And run the interpolator.
        # [xy]spline() does a meshgrid-like broadcast, so fxi,fyi have
        # shape n(iyo),n(ixo)
        #
        # f[xy]i: floating-point pixel coords in the input image
        fxi = xspline(ixo, iyo).T.astype(np.float32)
        fyi = yspline(ixo, iyo).T.astype(np.float32)

        if ps:
            plt.clf()
            plt.plot(ixo, np.zeros_like(ixo), 'r,')
            plt.plot(np.zeros_like(iyo), iyo, 'm,')
            plt.plot(ixo, max(iyo) + np.zeros_like(ixo), 'r,')
            plt.plot(max(ixo) + np.zeros_like(iyo), iyo, 'm,')
            plt.plot([0,W,W,0,0], [0,0,H,H,0], 'k-')
            plt.title('C: Target image; i*o')
            expand_axes()
            ps.savefig()
            plt.clf()
            plt.plot(fxi, fyi, 'r,')
            plt.plot([0,w,w,0,0], [0,0,h,h,0], 'k-')
            plt.title('D: Input image, f*i')
            expand_axes()
            ps.savefig()

    else:
        # Use 2-d broadcasting pixel <-> radec functions here.
        # This can be rather expensive, with lots of WCS calls!

        R = targetwcs.pixelxy2radec(ixo[np.newaxis,:] + 1.,
                                    iyo[:,np.newaxis] + 1.)
        if len(R) == 3:
            # ok,ra,dec
            R = R[1:]
        ok,fxi,fyi = wcs.radec2pixelxy(*R)
        assert(np.all(ok))
        del ok
        fxi -= 1.
        fyi -= 1.

    # i[xy]i: int coords in the input image.
    itype = intType
    if len(Limages) and cinterp:
        # the lanczos3_interpolate function below requires int32!
        itype = np.int32

    # (f + 0.5).astype(int) is often faster than round().astype(int) or rint!
    ixi = (fxi + 0.5).astype(itype)
    iyi = (fyi + 0.5).astype(itype)

    # Cut to in-bounds pixels.
    I,J = np.nonzero((ixi >= 0) * (ixi < w) * (iyi >= 0) * (iyi < h))
    ixi = ixi[I,J]
    iyi = iyi[I,J]
    fxi = fxi[I,J]
    fyi = fyi[I,J]

    # i[xy]o: int coords in the target image.
    # These were 1-d arrays that got broadcasted
    iyo = iyo[0] + I.astype(intType)
    ixo = ixo[0] + J.astype(intType)
    del I,J

    if spline and ps:
        plt.clf()
        plt.plot(ixo, iyo, 'r,')
        plt.plot([0,W,W,0,0], [0,0,H,H,0], 'k-')
        plt.title('E: Target image; i*o')
        expand_axes()
        ps.savefig()
        plt.clf()
        plt.plot(fxi, fyi, 'r,')
        plt.plot([0,w,w,0,0], [0,0,h,h,0], 'k-')
        plt.title('F: Input image, f*i')
        expand_axes()
        ps.savefig()

    assert(np.all(ixo >= 0))
    assert(np.all(iyo >= 0))
    assert(np.all(ixo < W))
    assert(np.all(iyo < H))

    assert(np.all(ixi >= 0))
    assert(np.all(iyi >= 0))
    assert(np.all(ixi < w))
    assert(np.all(iyi < h))

    if len(Limages):
        dx = (fxi - ixi).astype(np.float32)
        dy = (fyi - iyi).astype(np.float32)
        del fxi
        del fyi

        # Lanczos interpolation.
        # number of pixels
        nn = len(ixo)
        NL = 2*L+1
        # accumulators for each input image
        laccs = [np.zeros(nn, np.float32) for im in Limages]

        if cinterp:
            from lanczos.lanczos import lanczos3_interpolate            
            rtn = lanczos3_interpolate(ixi, iyi, dx, dy, laccs,
                                       [lim.astype(np.float32) for lim in Limages])
        else:
            _lanczos_interpolate(L, ixi, iyi, dx, dy, laccs, Limages, table=table)
        rims = laccs
    else:
        rims = []

    # 1-D output
    if oned:
        return (iyo,ixo, iyi,ixi, rims)  # i-input, o-output
    # 2-D output
    else:
        rims2 = []
        masks = []
        for i in range(len(Limages)):
            newim = np.zeros([H,W],Limages[i].dtype)+np.nan
            newim[iyo,ixo] = rims[i]
            rims2.append(newim)
            mask = np.zeros([H,W],bool)
            mask[iyo,ixo] = True
            masks.append(mask)
        # Only one and list not input, strip outer list layer
        if listinput==False:
            rims2 = rims2[0]
            masks = masks[0]

        return rims2,masks
    

def _lanczos_interpolate(L, ixi, iyi, dx, dy, laccs, limages,
                         table=True):
    '''
    L: int, Lanczos order
    ixi: int, 1-d numpy array, len n, x coord in input images
    iyi:     ----""----        y
    dx: float, 1-d numpy array, len n, fractional x coord
    dy:      ----""----                    y
    laccs: list of [float, 1-d numpy array, len n]: outputs
    limages list of [float, 2-d numpy array, shape h,w]: inputs
    '''
    #from astrometry.util.miscutils import lanczos_filter
    from lanczos import lanczos_filter
    lfunc = lanczos_filter
    if L == 3:
        try:
            #from astrometry.util import lanczos3_filter, lanczos3_filter_table
            from lanczos import lanczos3_filter, lanczos3_filter_table
            # 0: no rangecheck
            if table:
                lfunc = lambda nil,x,y: lanczos3_filter_table(x,y, 1)
            else:
                lfunc = lambda nil,x,y: lanczos3_filter(x,y)
        except:
            pass

    h,w = limages[0].shape
    n = len(ixi)
    # sum of lanczos terms
    fsum = np.zeros(n)
    off = np.arange(-L, L+1)
    fx = np.zeros(n, np.float32)
    fy = np.zeros(n, np.float32)
    for oy in off:
        lfunc(L, -oy + dy, fy)
        for ox in off:
            lfunc(L, -ox + dx, fx)
            for lacc,im in zip(laccs, limages):
                lacc += fx * fy * im[np.clip(iyi + oy, 0, h-1),
                                     np.clip(ixi + ox, 0, w-1)]
                fsum += fx*fy
    for lacc in laccs:
        lacc /= fsum


