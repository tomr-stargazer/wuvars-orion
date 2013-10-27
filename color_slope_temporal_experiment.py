"""
A script to figure out whether the distribution of color slopes
is a function of how long you observe or how many times you observe.

Incidentally, this kind of thing might also be a good strategy for 
discovering or selecting variables who change their variability mechanism 
in our observations. (currently, we're scanning by eye).

This could ALSO be used to plot typical variability amplitudes versus 
time baseline, especially as a function of variable class.

"""

from __future__ import division

import numpy as np
import atpy


def calculate_color_slope_ratios_versus_time_baseline():
    """
    Calculates the color slope ratios for each possible time baseline.

    """

    # For a bunch of different delta-t's...

      # For a bunch of different obs_initial's...

        # Calculate a spreadsheet for the "maxvars", "minimum" or "variables_data" photometry table

        # Extract the stars with "good data" in this regime (probably just confirm that it's in autovars_true)

        # then run color_slope_filtering on it...

        # and extract which guys have colors in the relevant ranges!


    color_slope_ratios_table = atpy.Table()

    addc = color_slope_ratios_table.add_column

    addc("time_baseline", time_baseline)
    addc("n_positive_slope", n_positive_slope)
    addc("n_negative_slope", n_negative_slope)
    addc("n_indef_slope", n_undef_slope)
    addc("n_obs", n_obs)
    
    return color_slope_ratios_table



def plot_color_slope_ratios_versus_time_baseline():
    """
    Plot color slope ratios versus time baseline.

    Also consider plotting "number of stars with significant color variability"
    versus time baseline.

    This will intrinsically be a scatterplot.
    Points with more observations in them may deserve bigger dots or something.

    """
    
    pass
