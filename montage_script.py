"""
This is a script to help us generate lots of lightcurves and, 
for periodics, glue together various plots.
"""

from subprocess import call

import numpy as np

import atpy

import plot3

path1 = "/home/tom/reu/ORION/DATA/subjective/periodic_book/"
path2 = "/home/tom/reu/ORION/DATA/subjective/periodic_book/glued/"
path3 = "/home/tom/reu/ORION/DATA/subjective/nonperiodic_book/"

subjective_periodics = atpy.Table("/home/tom/reu/ORION/DATA/subjective/subjective_periodic_candidate_spreadsheet.fits")

subjective_nonpers = atpy.Table("/home/tom/reu/ORION/DATA/subjective/subjective_nonperiod_candidate_spreadsheet.fits")

data = atpy.Table('/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5.fits')

def gen_periodic_plots(start=0):
    """ 
    Makes glued 3-panel plots for all of the periodic variable candidates
    """

    for s in subjective_periodics.SOURCEID[start:]:
        # Let's make 3 plots. LC, folded, and pgram. Save em all into a place.

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True,
                        outfile=path1+"%s_lc.png"%str(s))

        plot3.graded_phase(data, s, timecolor='time', 
                           period=subjective_periodics.best_period[
                subjective_periodics.SOURCEID==s][0], 
                           color_slope=True, outfile=path1+"%s_phase.png"%str(s))

        try:
            plot3.lsp_power(data, s, outfile=path1+"%s_pgram.png"%str(s))
        except Exception, e:
            print "periodogram failed for %s" % str(s)
            print e


        # now glue em together!

        call(["montage","-mode", "concatenate", "-tile", "2x", 
             path1+"%s_*.png" % str(s), path2+"%s-glued.png" % str(s) ])

        return

def gen_nonper_lc(start=0):
    """ Makes lightcurves for nonperiodic variable candidates. """

    for s in subjective_nonpers.SOURCEID[start:]:

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True,
                        outfile=path3+"%s_lc.png"%str(s))

    return
