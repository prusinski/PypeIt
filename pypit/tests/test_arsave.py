# Module to run tests on arsave
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import numpy as np
import pytest

from astropy import units
from astropy.io import fits

from pypit import arparse as settings
from pypit import arsciexp
from pypit import arspecobj
from pypit.core import arsort
from pypit import arsave

def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)


def mk_specobj(flux=5, objid=500):
    # specobj
    npix = 100
    specobj = arspecobj.SpecObjExp((100,100), 'Kast', 0, 0, (0.4,0.6), 0.5, 0.5, objtype='science')
    specobj.boxcar = dict(wave=np.arange(npix)*units.AA, counts=np.ones(npix)*flux)
    specobj.optimal = dict(wave=np.arange(npix)*units.AA, counts=np.ones(npix)*flux-0.5)
    specobj.objid = objid
    specobj.trace = np.arange(npix) / npix
    # Return
    return specobj


def test_save2d_fits():
    settings.dummy_settings()
    #fitsdict = arutils.dummy_fitsdict(nfile=1, spectrograph='none', directory=data_path(''))
    fitstbl = arsort.dummy_fitstbl(directory=data_path(''))
    # Kludge
    fitstbl.remove_column('filename')
    fitstbl['filename'] = 'b1.fits.gz'
    # Dummy self
    slf = arsciexp.dummy_self(fitstbl=fitstbl)
    # Settings
    settings.argflag['run']['directory']['science'] = data_path('')
    settings.argflag['reduce']['masters']['setup'] = 'A_01_aa'
    # Fill with dummy images
    dum = np.ones((100,100))
    slf._sciframe[0] = dum
    slf._modelvarframe[0] = dum * 2
    slf._bgframe[0] = dum + 0.1
    slf._basename = 'test'
    slf._idx_sci[0] = 0
    # Call
    arsave.save_2d_images(slf, fitstbl)
    # Read and test
    head0 = fits.getheader(data_path('spec2d_test.fits'))
    assert head0['PYPCNFIG'] == 'A'
    assert head0['PYPCALIB'] == 'aa'
    assert 'PYPIT' in head0['PIPELINE']


def test_save1d_fits():
    """ save1d to FITS and HDF5
    """
    settings.dummy_settings()
    fitstbl = arsort.dummy_fitstbl(spectrograph='shane_kast_blue', directory=data_path(''))
    # Dummy self
    slf = arsciexp.dummy_self(fitstbl=fitstbl)
    slf._specobjs = []
    slf._specobjs.append([])
    slf._specobjs[0].append([mk_specobj()])
    # Write to FITS
    arsave.save_1d_spectra_fits(slf._specobjs, fitstbl[5], data_path('tst.fits'))


def test_save1d_hdf5():
    """ save1d to FITS and HDF5
    """
    # Dummy self
    fitstbl = arsort.dummy_fitstbl(spectrograph='shane_kast_blue', directory=data_path(''))
    slf = arsciexp.dummy_self(fitstbl=fitstbl)
    # specobj
    slf._specobjs = []
    slf._specobjs.append([])
    slf._specobjs[0].append([mk_specobj(objid=455), mk_specobj(flux=3., objid=555)])
    # Write to HDF5
    arsave.save_1d_spectra_hdf5(slf, fitstbl)

