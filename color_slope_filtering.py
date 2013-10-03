"""
This is a script for calculating color slopes! Its products are used
by other scripts.

Some of the parameters I've chosen are inspired by Fig. 20 from 
Carpenter, Hillenbrand & Skrutskie 2001:
"Only variable stars in which the observed rms of the appropriate colors or magnitudes exceeded the expected rms by a factor of 1.5 are shown. The open histograms are for all stars that meet these criteria, and the hatched histograms are those stars in which the slope have been determined to an accuracy of better than 20%."

"""

from official_star_counter import *


def filter_color_slopes(data, color, noise_threshold=1.5, slope_confidence=0.2):
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
    color : {'jh', 'hk', or 'jhk'}
        Which color term to filter on. The relevant colors will
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
    filtered_data : atpy.Table
        Subset of `data` filtered by color slopes that meet our criteria.
    
    """

    valid_colors = ['jh', 'hk', 'jhk']
    if color.lower() not in valid_colors:
        raise ValueError("Invalid color! Use 'jh', 'hk', or 'jhk'.")

    # Let's break this into two cases. 1. Doing all of JHK
    if color.lower() == 'jhk':
        filtered_data_soft = data.where(
            (data.hmk_rmsr > noise_threshold * data.hmk_err_meanr) &
             (data.jmh_rmsr > noise_threshold * data.jmh_err_meanr) )

        if slope_confidence:
            filtered_data = filtered_data_soft.where(
                filtered_data_soft.jhk_slope_err <
                np.abs( slope_confidence * filtered_data_soft.jhk_slope))

            return filtered_data
        else:
            return filtered_data_soft

    # Case 2. Doing J-H or H-K
    else:
        faintness_cutoff = {'j': 17, 'h': 16, 'k': 16}

        blue_band, red_band = color.lower()
        color_with_m = blue_band + 'm' + red_band

        N_blue = 'N_'+blue_band
        blue_mean = blue_band+'_mean'
        N_blue_info = 'N_'+blue_band+'_info'

        N_red = 'N_'+red_band
        red_mean = red_band+'_mean'
        N_red_info = 'N_'+red_band+'_info'

        color_rmsr = color_with_m + '_rmsr'
        color_err_meanr = color_with_m + '_err_meanr'

        # Blue and Red pristine - copied from "case1" re: official_star_counter
        filtered_data_soft = data.where(
        (    # BLUE band criteria
            (data[N_blue] >= 50) & (data[N_blue] <= 125) &
            (data[blue_mean] > 11) &
            (data[blue_mean] < faintness_cutoff[blue_band]) &
            (data[N_blue_info] == 0)
            ) &
        (   # RED band criteria
            (data[N_red] >= 50) & (data[N_red] <= 125) &
            (data[red_mean] > 11) &
            (data[red_mean] < faintness_cutoff[red_band]) &
            (data[N_red_info] == 0)
            ) &
        # Blue-Red variability criterion
        (data[color_rmsr] > noise_threshold * data[color_err_meanr]) )

        if slope_confidence:

            if color == 'jh':
                color_slope = 'jjh_slope'
            else:
                color_slope = 'khk_slope'

            color_slope_err = color_slope+'_err'

            filtered_data = filtered_data_soft.where(
                filtered_data_soft[color_slope_err] <
                np.abs( slope_confidence * filtered_data_soft[color_slope]))

            return filtered_data
        else:
            return filtered_data_soft

# We provide these to anyone who doesn't want to think too hard.
jhk_empty = filter_color_slopes(autovars_strict, 'jhk', slope_confidence=None)
jhk_filled = filter_color_slopes(autovars_strict, 'jhk')

jh_empty = filter_color_slopes(autovars_true, 'jh', slope_confidence=None)
jh_filled = filter_color_slopes(autovars_true, 'jh')

hk_empty = filter_color_slopes(autovars_true, 'hk', slope_confidence=None)
hk_filled = filter_color_slopes(autovars_true, 'hk')
