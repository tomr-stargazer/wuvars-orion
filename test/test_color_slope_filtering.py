from __future__ import division

from color_slope_filtering import *

def test_that_old_arrays_dont_change():

    assert len(jhk_filled) == len(jhk_empty) == 69

    assert len(hk_filled) == 92
    assert len(hk_empty) == 129

    assert len(jh_filled) == 88
    assert len(jh_empty) == 103

