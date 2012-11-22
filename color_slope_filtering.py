"""
This is a script for calculating color slopes! Its products are used
by other scripts.
"""

from official_star_counter import *


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

