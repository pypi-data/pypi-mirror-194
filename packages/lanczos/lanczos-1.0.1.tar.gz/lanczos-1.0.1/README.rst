
Lanczos
=======

Image resampling using Lanczos interpolation.
Redistribution and repackaging of code by Dustin Lang in 
`Astrometry.net <https://github.com/dstndstn/astrometry.net>`_
under the 3-clause BSD-style license.
More flexibility for astropy WCS and documentated added by David Nidever.

Install
-------

Lanczos can be most easily installed using ``pip``.  This should automatically deal with all of the C compilations.

.. code-block:: unix

    pip install lanczos

You can also git clone and python setup install.

.. code-block:: unix

    git clone git@github.com:dnidever/lanczos.git
    python setup.py install

    
Examples
--------

.. code-block:: python

    from astropy.io import fits
    from astropy.wcs import WCS
    from lanczos.resample import resample_with_wcs

    im,head = fits.getdata('myimage.fits',header=True)
    wcs = WCS(head)

    # Create a new WCS object.  The number of axes must be set
    # from the start
    targetwcs = WCS(naxis=2)
    targetwcs.wcs.crpix = [2000,2000]
    targetwcs.wcs.cdelt = np.array([0.00012828,0.00012828])
    targetwcs.wcs.crval = [34.7180219946,  57.1575336869]
    targetwcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    targetwcs.array_shape = [4000,4000]

    rim,mask = resample.resample_with_wcs(targetwcs,wcs,im)

