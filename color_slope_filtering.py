"""
This is a script for calculating color slopes! Its products are used
by other scripts.

Some of the parameters I've chosen are inspired by Fig. 20 from 
Carpenter, Hillenbrand & Skrutskie 2001:
"Only variable stars in which the observed rms of the appropriate colors or magnitudes exceeded the expected rms by a factor of 1.5 are shown. The open histograms are for all stars that meet these criteria, and the hatched histograms are those stars in which the slope have been determined to an accuracy of better than 20%."

"""

from official_star_counter import *


def filter_color_slopes(data, band, noise_threshold=1.5, slope_confidence=0.2):
    """
    Filters color slopes on quality. Returns a sub-table with good cslopes.

    By default we filter both on magnitude of color change 
    (relative to photometric noise) and on confidence on the fitted 
    color slope. You can optionally disable the slope confidence filter.

    Parameters
    ----------
    data : atpy.Table
        Table of spreadsheet data (including previously calculated
        color slopes) on the stars in question.
    band : {'jh', 'hk', or 'jhk'}
        Which color term to filter on. The relevant bands will
        be ensured for quality.
    noise_threshold : float, optional, default: 1.5
        How many times above the expected photometric noise
        do you require the rms color variability to be?
        Try not to go below 1.0. The default choice of 1.5 is
        inspired by Carpenter et al. 2001.
    slope_confidence : float, optional, default: 0.2
        How small should the uncertainty be on a slope for us
        to include it? The default choice of 20% is also
        inspired by Carpenter er al. 2001.

    Returns
    -------
    filtered_table : atpy.Table
        Subset of `data` filtered by color slopes that meet our criteria.
    
    """

    good_bands = ['jh', 'hk', 'jhk']
    if band not in good_bands:
        raise ValueError("Invalid band! Use 'jh', 'hk', or 'jhk'.")

    

# How much more than noise do we want the "color variability" cutoff to be?
noise_threshold = 1.5

# How confident do we want to have our filled-in slopes be?
slope_confidence = 0.2

# J-H vs H-K slopes

jhk_empty = autovars_strict.where(
    (autovars_strict.hmk_rmsr > noise_threshold * 
     autovars_strict.hmk_err_meanr) & 
    (autovars_strict.jmh_rmsr > noise_threshold * 
     autovars_strict.jmh_err_meanr) )
jhk_filled = jhk_empty.where(
    jhk_empty.jhk_slope_err < 
    np.abs( slope_confidence * jhk_empty.jhk_slope))

at = autovars_true

# J vs J-H slopes

jh_empty = at.where( 
    # J and H pristine - copied from "case1" re: official_star_counter
    (
    (at.N_j >= 50) & (at.N_j <= 125) &    # J band criteria
    (at.j_mean > 11) & (at.j_mean < 17) & 
    (at.N_j_info == 0) 
    ) &
      (
    (at.N_h >= 50) & (at.N_h <= 125) &    # H band criteria
    (at.h_mean > 11) & (at.h_mean < 16) & 
    (at.N_h_info == 0) 
    ) & 
    # J-H variability criterion
    (at.jmh_rmsr > noise_threshold * 
     at.jmh_err_meanr) )

jh_filled = jh_empty.where(
    jh_empty.jjh_slope_err < 
    np.abs( slope_confidence * jh_empty.jjh_slope))

# K vs H-K slopes

hk_empty = at.where(
    # H and K pristine - copied from "case1" re: official_star_counter
    (
    (at.N_h >= 50) & (at.N_h <= 125) &    # H band criteria
    (at.h_mean > 11) & (at.h_mean < 16) & 
    (at.N_h_info == 0) 
    ) &
      (
    (at.N_k >= 50) & (at.N_k <= 125) &    # K band criteria
    (at.k_mean > 11) & (at.k_mean < 16) & 
    (at.N_k_info == 0) 
    ) & 
    # H-K variability criterion
    (at.hmk_rmsr > noise_threshold * 
     at.hmk_err_meanr) )

hk_filled = hk_empty.where(
    hk_empty.khk_slope_err < 
    np.abs( slope_confidence * hk_empty.khk_slope))

