import pynbody
from pynbody.halo.adaptahop import AdaptaHOPCatalogue

from scipy.io import FortranFile as FF
import numpy as np


def test_load_adaptahop_catalogue():
    f = pynbody.load('testdata/output_00080')
    h = f.halos()
    assert len(h) == h._headers['nhalos'] + h._headers['nsubs']

def test_load_one_halo():
    f = pynbody.load('testdata/output_00080')
    h = f.halos()
    np.testing.assert_allclose(h[1].properties['members'], h[1]['iord'])

def test_get_group():
    f = pynbody.load('testdata/output_00080')
    h = f.halos()

    group_array = h.get_group_array()
    iord = f.dm['iord']

    for halo_id in range(1, len(h)+1):
        mask = group_array == halo_id

        # Check that the indices
        # - read from halo (h[halo_id]['iord'])
        # - obtained from get_group_array masking
        # are the same (in term of sets)
        assert len(np.setdiff1d(iord[mask], h[halo_id]['iord'])) == 0
        assert len(np.setdiff1d(h[halo_id]['iord']), iord[mask]) == 0


def test_halo_particle_ids():
    f = pynbody.load('testdata/output_00080')
    h = f.halos()

    with FF(h._fname, mode="r") as f:
        for halo_id in range(1, len(h)+1):
            # Manually read the particle ids and make sure pynbody is reading them as it should
            f._fp.seek(h[halo_id].properties["file_offset"])

            f.read_ints()  # number of particles
            expected_members = f.read_ints("i")  # halo members

            np.testing.assert_equal(expected_members, h[halo_id].properties['members'])