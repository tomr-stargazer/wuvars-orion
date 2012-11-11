"""
This is a script to help us generate lots of lightcurves and, 
for periodics, glue together various plots.
"""

import numpy as np

import atpy

import plot3

path1 = "/home/tom/reu/ORION/DATA/subjective/periodic_book"

subjective_periodics = atpy.Table("/home/tom/reu/ORION/DATA/subjective/subjective_periodic_candidate_spreadsheet.fits")

data = atpy.Table('/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5.fits')

for s in subjective_periodics.SOURCEID:
    # Let's make 3 plots. LC, folded, and pgram. Save em all into a place.
    
    plot3.graded_lc(data, s, abridged=True, color_slope=True, timecolor=True)

    plot3.graded_phase(data, s, timecolor='time', 
                       period=subjective_periodics.best_period[
            subjective_periodics.SOURCEID==s], 
                       
