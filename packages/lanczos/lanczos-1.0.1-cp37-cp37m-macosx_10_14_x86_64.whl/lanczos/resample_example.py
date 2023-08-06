# This file is part of the Astrometry.net suite.
# Licensed under a 3-clause BSD style license - see LICENSE
from __future__ import print_function
from __future__ import absolute_import
import numpy as np

class ResampleError(Exception):
    pass
class OverlapError(ResampleError):
    pass
class NoOverlapError(OverlapError):
    pass
class SmallOverlapError(OverlapError):
    pass



if __name__ == '__main__':
    import fitsio
    from astrometry.util.util import Sip,Tan
    import time
    import sys
    import pylab as plt

    from astrometry.util.util import lanczos3_filter, lanczos3_filter_table
    # x = np.linspace(-4, 4, 500)
    # L = np.zeros_like(x)
    # L2 = np.zeros(len(x), np.float32)
    # lanczos3_filter(x, L)
    # lanczos3_filter_table(x.astype(np.float32), L2, 1)
    # plt.clf()
    # plt.plot(x, L, 'r-')
    # plt.plot(x, L2, 'b-')
    # plt.savefig('l1.png')

    x = np.linspace(-3.5, 4.5, 8192).astype(np.float32)
    L1 = np.zeros_like(x)
    L2 = np.zeros_like(x)
    lanczos3_filter(x, L1)
    lanczos3_filter_table(x, L2, 1)
    print('L2 - L1 RMS:', np.sqrt(np.mean((L2-L1)**2)))
    
    if True:
        ra,dec = 0.,0.,
        pixscale = 1e-3
        W,H = 10,1

        cowcs = Tan(ra, dec, (W+1)/2., (H+1)/2.,
                    -pixscale, 0., 0., pixscale, W, H)
        dx,dy = 0.25, 0.
        wcs = Tan(ra, dec, (W+1)/2. + dx, (H+1)/2. + dy,
                  -pixscale, 0., 0., pixscale, W, H)

        pix = np.zeros((H,W), np.float32)
        pix[0,W//2] = 1.
        
        Yo,Xo,Yi,Xi,(cpix,) = resample_with_wcs(cowcs, wcs, [pix], 3)
        print('C', cpix)
        Yo2,Xo2,Yi2,Xi2,(pypix,) = resample_with_wcs(cowcs, wcs, [pix], 3, cinterp=False, table=False)
        print('Py', pypix)

        print('RMS', np.sqrt(np.mean((cpix - pypix)**2)))
        
        sys.exit(0)
        
        
    if True:
        ra,dec = 219.577111, 54.52
        pixscale = 2.75 / 3600.
        W,H = 10,10
        cowcs = Tan(ra, dec, (W+1)/2., (H+1)/2.,
                    -pixscale, 0., 0., pixscale, W, H)

        for i,(dx,dy) in enumerate([(0.01, 0.02),
                                    (0.1, 0.0),
                                    (0.2, 0.0),
                                    (0.3, 0.0),
                                    (0.4, 0.0),
                                    (0.5, 0.0),
                                    (0.6, 0.0),
                                    (0.7, 0.0),
                                    (0.8, 0.0),
                                    ]):
            wcs = Tan(ra, dec, (W+1)/2. + dx, (H+1)/2. + dy,
                      -pixscale, 0., 0., pixscale, W, H)
            pix = np.zeros((H,W), np.float32)
            pix[H/2, :] = 1.
            pix[:, W/2] = 1.
    
            Yo,Xo,Yi,Xi,(cpix,) = resample_with_wcs(cowcs, wcs, [pix], 3)
            Yo2,Xo2,Yi2,Xi2,(pypix,) = resample_with_wcs(cowcs, wcs, [pix], 3, cinterp=False)
            cim = np.zeros((H,W))
            cim[Yo,Xo] = cpix
            pyim = np.zeros((H,W))
            pyim[Yo2,Xo2] = pypix

            plt.clf()
            plt.plot(cim[0,:], 'b-', alpha=0.5)
            plt.plot(cim[H/4,:], 'c-', alpha=0.5)
            plt.plot(pyim[0,:], 'r-', alpha=0.5)
            plt.plot(pyim[H/4,:], 'm-', alpha=0.5)
            plt.plot(1000. * (cim[0,:] - pyim[0,:]), 'k-', alpha=0.5)
            plt.savefig('p2-%02i.png' % i)
        sys.exit(0)
    
    ra,dec = 219.577111, 54.52
    pixscale = 2.75 / 3600.
    #W,H = 2048, 2048
    W,H = 512, 512
    #W,H = 100,100
    cowcs = Tan(ra, dec, (W+1)/2., (H+1)/2.,
                -pixscale, 0., 0., pixscale, W, H)
    cowcs.write_to('co.wcs')
    
    if True:
        #intfn = '05579a167-w1-int-1b.fits'
        intfn = 'wise-frames/9a/05579a/167/05579a167-w1-int-1b.fits'
        wcs = Sip(intfn)
        pix = fitsio.read(intfn)
        pix[np.logical_not(np.isfinite(pix))] = 0.
        print('pix', pix.shape, pix.dtype)

    
    for i in range(5):
        t0 = time.clock()
        Yo,Xo,Yi,Xi,ims = resample_with_wcs(cowcs, wcs, [pix], 3)
        t1 = time.clock() - t0
        print('C resampling took', t1)

    t0 = time.clock()
    Yo2,Xo2,Yi2,Xi2,ims2 = resample_with_wcs(cowcs, wcs, [pix], 3, cinterp=False, table=False)
    t2 = time.clock() - t0
    print('py resampling took', t2)
    
    out = np.zeros((H,W))
    out[Yo,Xo] = ims[0]
    fitsio.write('resampled-c.fits', out, clobber=True)
    cout = out
    
    out = np.zeros((H,W))
    out[Yo,Xo] = ims2[0]
    fitsio.write('resampled-py.fits', out, clobber=True)
    pyout = out

    plt.clf()
    plt.imshow(cout, interpolation='nearest', origin='lower')
    plt.colorbar()
    plt.savefig('c.png')
    plt.clf()
    plt.imshow(pyout, interpolation='nearest', origin='lower')
    plt.colorbar()
    plt.savefig('py.png')

    plt.clf()
    plt.imshow(cout - pyout, interpolation='nearest', origin='lower')
    plt.colorbar()
    plt.savefig('diff.png')

    print('Max diff:', np.abs(cout - pyout).max())

