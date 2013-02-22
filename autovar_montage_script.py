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
hivar_path = "/home/tom/reu/ORION/DATA/autovar/hivar/"
hivar_per_path = "/home/tom/reu/ORION/DATA/autovar/hivar/per/"
hivar_per_path_g = "/home/tom/reu/ORION/DATA/autovar/hivar/glued/"

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


# Let's make a function that does periods for "high-variables".

hivar = autovars_true.where(autovars_true.Stetson > 20)
hivar_periodics = autovars_true_periodics.where(
    autovars_true_periodics.Stetson > 20)
hivar_nonpers = autovars_true_nonpers.where(
    autovars_true_nonpers.Stetson > 20)


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

# START HIVAR HIJINKS HIJACK

def gen_hivar_periodic_plots(start=0):
    """ 
    Makes glued 3-panel plots for all of the periodic hivars.
    """
    
    counter = 1
    c_max = len(hivar_periodics)

    tables_of_periodics = [autovars_true_periods, autovars_true_periods_s1]

    print 'lol'
    for t in tables_of_periodics:
        print 'lol2'
        # first, the s123 periodics (more than 95% of them)
        for s in t.SOURCEID[start:]:
            # If this is a strict autovar, we give it special stuff.
            if s not in hivar.SOURCEID: continue
            if s in autovars_strict.SOURCEID:
                flag = "s_"
            else:
                flag = ""

            # Let's make 3 plots. LC, folded, and pgram. Save em all into a place.
            plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                            timecolor=True, name=flag+str(s),
                            outfile=hivar_per_path+"%s_lc.png"%str(s))


            plot3.graded_phase(data, s, timecolor='time', 
                               name=flag+str(s),
                               period=t.best_period[t.SOURCEID==s], 
                               color_slope=True, outfile=hivar_per_path+"%s_phase.png"%str(s))

            try:
                plot3.lsp_power(data, s, outfile=hivar_per_path+"%s_pgram.png"%str(s))
            except Exception, e:
                print "periodogram failed for %s" % str(s)
                print e


            # now glue em together!
            call(["montage","-mode", "concatenate", "-tile", "2x", 
                 hivar_per_path+"%s_*.png" % str(s), 
                  hivar_per_path_g+flag+"%s-glued.png" % str(s) ])


            print "Completed plot %d of %d" % (counter, c_max)
            counter += 1
        
    return

def gen_hivar_nonper_lc(start=0):
    """ Makes lightcurves for nonperiodic hivars. """

    counter = 1
    c_max = len(hivar_nonpers)

    for s in autovars_true_nonpers.SOURCEID[start:]:

        if s not in hivar.SOURCEID: continue
        # If this is a strict autovar, we give it special stuff.
        if s in autovars_strict.SOURCEID:
            flag = "s_"
        else:
            flag = ""

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True, name=flag+str(s),
                        outfile=hivar_path+flag+"%s_lc.png"%str(s))

        print "Completed plot %d of %d" % (counter, c_max)
        counter += 1

    return


def suffix_generator(table, index):
    """
    Builds an ONCvar suffix from the flags on a given source.

    Suffixes look like ('a'|'t'|'j')+('p'|'n'), for
    'a': autovar
    't': strict autovar
    'j': subjective var
    'p': periodic variable
    'n': nonperiodic variable

    Parameters
    -----------
    table : atpy.Table
        The statistics table. Must have the `automatic`, `strict`, 
        and `periodic` columns.
    index : int
        Which star in the table to extract? Note this is NOT the ONCvar ID,
        but is offset from it by one.

    Returns
    -------
    suffix : str
        A string of length two, matching the following pattern:
        ('a'|'t'|'j')+('p'|'n') (e.g. "ap", "jp", "tn", "jn")

    """
    
    if table.autovar == 0:
        first = 'j'
    elif table.strict == 1:
        first = 't'
    else:
        first = 'a'
        
    if table.periodic == 1:
        second = 'p'
    else:
        second = 'n'
        
    suffix = first+second
    return suffix



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



