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

path4 = '/home/tom/reu/ORION/DATA/subjective/confirmed_book/periodic/'
path5 = '/home/tom/reu/ORION/DATA/subjective/confirmed_book/periodic/glued/'
path6 = '/home/tom/reu/ORION/DATA/subjective/confirmed_book/nonperiodic/'

#for new dudes
path7 = "/home/tom/reu/ORION/DATA/subjective/new_periodic_book/"
path8 = "/home/tom/reu/ORION/DATA/subjective/new_periodic_book/glued/"
path9 = "/home/tom/reu/ORION/DATA/subjective/new_nonperiodic_book/"


subjective_periodics = atpy.Table("/home/tom/reu/ORION/DATA/subjective/subjective_periodic_candidate_spreadsheet.fits")

conf_subj_periodics = atpy.Table("/home/tom/reu/ORION/DATA/subjective/subjective_periodics_confirmed_spread.fits")

new_conf_subj_periodics = atpy.Table("/home/tom/reu/ORION/DATA/subjective/new_subjective_periodics_confirmed_spread.fits")

subjective_nonpers = atpy.Table("/home/tom/reu/ORION/DATA/subjective/subjective_nonperiod_candidate_spreadsheet.fits")

conf_subj_nonpers = atpy.Table("/home/tom/reu/ORION/DATA/subjective/subjective_nonpers_confirmed_spread.fits")

new_conf_subj_nonpers = atpy.Table("/home/tom/reu/ORION/DATA/subjective/new_subjective_nonpers_confirmed_spread.fits")

# this is for the new dudes
new_subjective_periodics = atpy.Table("/home/tom/reu/ORION/DATA/subjective/new_subjective_periodic_candidate_spreadsheet.fits")

new_subjective_nonpers = atpy.Table("/home/tom/reu/ORION/DATA/subjective/new_subjective_nonperiod_candidate_spreadsheet.fits")

data = atpy.Table('/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5.fits')


### This is where we conjoin the "new" guys to the "old" guys.

conf_subj_periodics.remove_columns(
    ['stats', "CONFIRMED PERIODIC", "CONFIRMED VARIABLE"])
new_conf_subj_periodics.remove_columns(
    ["CONFIRMED_PERIODIC", "CONFIRMED_VARIABLE"])
conf_subj_periodics.append( new_conf_subj_periodics )

new_conf_subj_nonpers.remove_columns(
    ['pstar_mean', 'pstar_median', 'pstar_rms'])
conf_subj_nonpers.append( new_conf_subj_nonpers)


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

def gen_conf_periodic_plots(start=0):
    """ 
    Makes glued 3-panel plots for all the CONFIRMED subjective periodic variables.
    """

    for s in conf_subj_periodics.SOURCEID[start:]:
        # Let's make 3 plots. LC, folded, and pgram. Save em all into a place.

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True,
                        outfile=path4+"%s_lc.png"%str(s))

        plot3.graded_phase(data, s, timecolor='time', 
                           period=conf_subj_periodics.best_period[
                conf_subj_periodics.SOURCEID==s][0], 
                           color_slope=True, outfile=path4+"%s_phase.png"%str(s))

        try:
            plot3.lsp_power(data, s, outfile=path4+"%s_pgram.png"%str(s))
        except Exception, e:
            print "periodogram failed for %s" % str(s)
            print e


        # now glue em together!

        call(["montage","-mode", "concatenate", "-tile", "2x", 
             path4+"%s_*.png" % str(s), path5+"%s-glued.png" % str(s) ])

    return

def gen_conf_nonper_lc(start=0):
    """ Makes lightcurves for CONFIRMED subjective nonperiodic variables. """

    for s in conf_subj_nonpers.SOURCEID[start:]:

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True,
                        outfile=path6+"%s_lc.png"%str(s))

    return

### Everything that follows is for the "NEW" subjectives.

def gen_new_periodic_plots(start=0):
    """ 
    Makes glued 3-panel plots for all of the NEW periodic variable candidates
    """

    for s in new_subjective_periodics.SOURCEID[start:]:
        # Let's make 3 plots. LC, folded, and pgram. Save em all into a place.

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True,
                        outfile=path7+"%s_lc.png"%str(s))

        plot3.graded_phase(data, s, timecolor='time', 
                           period=new_subjective_periodics.best_period[
                new_subjective_periodics.SOURCEID==s][0], 
                           color_slope=True, outfile=path7+"%s_phase.png"%str(s))

        try:
            plot3.lsp_power(data, s, outfile=path7+"%s_pgram.png"%str(s))
        except Exception, e:
            print "periodogram failed for %s" % str(s)
            print e


        # now glue em together!

        call(["montage","-mode", "concatenate", "-tile", "2x", 
             path7+"%s_*.png" % str(s), path8+"%s-glued.png" % str(s) ])

    return

def gen_new_nonper_lc(start=0):
    """ Makes lightcurves for nonperiodic variable candidates. """

    for s in new_subjective_nonpers.SOURCEID[start:]:

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True,
                        outfile=path9+"%s_lc.png"%str(s))

    return
