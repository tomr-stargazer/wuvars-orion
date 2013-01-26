"""
AUTOVARS version.

This is a script to help us generate lots of lightcurves and, 
for periodics, glue together various plots.
"""

from subprocess import call

import numpy as np

import atpy

import plot3
from official_star_counter import *

# let's rename these from `path1`... etc because they are unhelpful.

periodic_path = "/home/tom/reu/ORION/DATA/autovar/periodic/"
periodic_path_g = "/home/tom/reu/ORION/DATA/autovar/periodic/glued/"
nonper_path = "/home/tom/reu/ORION/DATA/autovar/nonperiodic/"

# Relevant variable names:
# ==Global==
# `autovars_true`: all automatically detected variables
# `autovars_strict`: all pristine auto-variables (a subset of `autovars_true`)
#==Periodics==
# `autovars_true_periodics`: subset of `autovars_true` who are periodic
# `autovars_strict_periodics`: subset of `autovars_strict` who are periodic
#==Non-periodic==
# `autovars_true_nonpers`: subset of `autovars_true` who are non-periodic
# `autovars_strict_nonpers`: subset of `autovars_strict` who are non-periodic

data = atpy.Table('/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5.fits')


def gen_autovar_periodic_plots(start=0):
    """ 
    Makes glued 3-panel plots for all of the periodic autovars.
    """
    
    counter = 1
    c_max = len(autovars_true_periodics)

    tables_of_periodics = [autovars_true_periods, autovars_true_periods_s1]

    for t in tables_of_periodics:

        # first, the s123 periodics (more than 95% of them)
        for s in t.SOURCEID[start:]:
            # If this is a strict autovar, we give it special stuff.
            if s in autovars_strict.SOURCEID:
                flag = "s_"
            else:
                flag = ""

            # Let's make 3 plots. LC, folded, and pgram. Save em all into a place.
            plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                            timecolor=True, name=flag+str(s),
                            outfile=periodic_path+"%s_lc.png"%str(s))


            plot3.graded_phase(data, s, timecolor='time', 
                               name=flag+str(s),
                               period=t.best_period[t.SOURCEID==s], 
                               color_slope=True, outfile=periodic_path+"%s_phase.png"%str(s))

            try:
                plot3.lsp_power(data, s, outfile=periodic_path+"%s_pgram.png"%str(s))
            except Exception, e:
                print "periodogram failed for %s" % str(s)
                print e


            # now glue em together!
            call(["montage","-mode", "concatenate", "-tile", "2x", 
                 periodic_path+"%s_*.png" % str(s), 
                  periodic_path_g+flag+"%s-glued.png" % str(s) ])


            print "Completed plot %d of %d" % (counter, c_max)
            counter += 1
        
    return

def gen_autovar_nonper_lc(start=0):
    """ Makes lightcurves for nonperiodic autovars. """

    counter = 1
    c_max = len(autovars_true_nonpers)

    for s in autovars_true_nonpers.SOURCEID[start:]:

        # If this is a strict autovar, we give it special stuff.
        if s in autovars_strict.SOURCEID:
            flag = "s_"
        else:
            flag = ""

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True, name=flag+str(s),
                        outfile=nonper_path+flag+"%s_lc.png"%str(s))

        print "Completed plot %d of %d" % (counter, c_max)
        counter += 1

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


