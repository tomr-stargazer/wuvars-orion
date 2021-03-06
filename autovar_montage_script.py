"""
AUTOVARS version.

This is a script to help us generate lots of lightcurves and, 
for periodics, glue together various plots.
"""

from subprocess import call
import os

import numpy as np

import atpy

import plot3
from official_star_counter import *
from montage_script import conf_subj_periodics

dropbox_bo_lightcurves = os.path.expanduser("~/Dropbox/Bo_Tom/lightcurve_book/")

# let's rename these from `path1`... etc because they are unhelpful.

periodic_path = "/home/tom/reu/ORION/DATA/autovar/periodic/"
periodic_path_g = "/home/tom/reu/ORION/DATA/autovar/periodic/glued/"
nonper_path = "/home/tom/reu/ORION/DATA/autovar/nonperiodic/"
hivar_path = "/home/tom/reu/ORION/DATA/autovar/hivar/"
hivar_per_path = "/home/tom/reu/ORION/DATA/autovar/hivar/per/"
hivar_per_path_g = "/home/tom/reu/ORION/DATA/autovar/hivar/glued/"
ukvar_path = "/home/tom/reu/ORION/DATA/ukvar/"
ukvar_path_ng = "/home/tom/reu/ORION/DATA/ukvar/unglued/"
lowvar_path = "/home/tom/reu/ORION/DATA/lowvar/"
lowvar_per_path = "/home/tom/reu/ORION/DATA/lowvar/periodic/"
lowvar_per_path_g = "/home/tom/reu/ORION/DATA/lowvar/periodic/glued/"

# Breaks from convention cause it's destined for dropbox.
jjh_path = dropbox_bo_lightcurves + "ukvar_jjh/"
jjh_path_g = dropbox_bo_lightcurves + "ukvar_jjh/glued/"

# Relevant variable names:
# ==Global==
# `autovars_true`: all automatically detected variables
# `autovars_strict`: all pristine auto-variables (a subset of `autovars_true`)
# `ukvar` : all variables minus clones! 
#==Periodics==
# `autovars_true_periodics`: subset of `autovars_true` who are periodic
# `autovars_strict_periodics`: subset of `autovars_strict` who are periodic
#==Non-periodic==
# `autovars_true_nonpers`: subset of `autovars_true` who are non-periodic
# `autovars_strict_nonpers`: subset of `autovars_strict` who are non-periodic

dropbox_bo_data = os.path.expanduser("~/Dropbox/Bo_Tom/data/")
dropbox_bo_aux_catalogs = os.path.expanduser("~/Dropbox/Bo_Tom/aux_catalogs/")

data = atpy.Table(dropbox_bo_data+"fdece_graded_clipped0.8_scrubbed0.1_dusted0.5.fits")

ukvar = atpy.Table(dropbox_bo_aux_catalogs+"UKvar_spreadsheet_withSIMBADnames_w1226_minusEasties_renamedOldONCvarColumn_w1227.fits")

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
    Builds a UKvar suffix from the flags on a given source.

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
        Which star in the table to extract? Note this is NOT the 
        UKvar ID, but is offset from it by one.

    Returns
    -------
    suffix : str
        A string of length two, matching the following pattern:
        ('a'|'t'|'j')+('p'|'n') (e.g. "ap", "jp", "tn", "jn")

    """
    
    if table.autovar[index] == 0:
        first = 'j'
    elif table.strict[index] == 1:
        first = 't'
    else:
        first = 'a'
        
    if table.periodic[index] == 1:
        second = 'p'
    else:
        second = 'n'
        
    suffix = first+second
    return suffix


# This is, unashamedly, a pure find-and-replace clone of `gen_oncvar_all()`.
# Which is to say, it was copied and pasted from the old oncvar thing.
def gen_ukvar_all(start=0, stop=len(ukvar)):
    """ 
    Creates all the UKvar plots in one shot.

    Uses the UKvar ID as the primary identifier; lists info
    in the filename distinguishing auto/strict/subj, plus per/nonper
    I'm thinking: 'a' for autovar, 't' for strict, 'j' for subj,
    'p' for periodic, 'n' for nonperiodic. Each dude gets two letters.

    if periodic:
        do the gluedvars stuff
    else:
        just a normal lightcurve!

    """

    for s, id, i in zip(ukvar.SOURCEID, ukvar.UKvar_ID, 
                        range(len(ukvar)))[start:stop]:

        # Each plot gets a suffix: ('a'|'t'|'j')+('p'|'n')
        
        suffix = suffix_generator(ukvar, i)

        # Periodics first

        if ukvar.periodic[i] == 1:
            
            # Dig up the best period for this dude! 3 main cases.

            if ukvar.autovar[i] == 1:
                if s in autovars_true_periods.SOURCEID:
                    t = autovars_true_periods
                elif s in autovars_true_periods_s1.SOURCEID:
                    t = autovars_true_periods_s1
                else:
                    raise Exception("Something weird happened!")
            else:
                t = conf_subj_periodics
                
            best_period = t.best_period[t.SOURCEID == s][0]

            # Let's make 3 plots. LC, folded, and pgram. Save em all into a place.
            # print out the names as ID_fs_lc.png
            plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                            timecolor=True,
                            name = "%s:  UKvar %s (%s)" %
                            (str(s), str(id), suffix),
                            outfile=ukvar_path_ng+"%s_%s_lc.png" %
                            (str(id), suffix))

            # ID_fs_phase.png
            plot3.graded_phase(data, s, timecolor='time', color_slope=True,
                               period=best_period, 
                               name = "%s:  UKvar %s (%s)" %
                               (str(s), str(id), suffix),
                               outfile=ukvar_path_ng+"%s_%s_phase.png" % 
                               (str(id), suffix))
            # ID_fs_pgram.png
            try:
                plot3.lsp_power(data, s, 
                                name = "%s:  UKvar %s (%s)" %
                                (str(s), str(id), suffix),
                                outfile=ukvar_path_ng+"%s_%s_pgram.png" %
                                (str(id), suffix))
            except Exception, e:
                print "periodogram failed for %s" % str(s)
                print e


# now glue em together!
                
            try:
                call(["montage","-mode", "concatenate", "-tile", "2x", 
                      ukvar_path_ng+"%s_%s*.png" % (str(id), suffix), 
                      ukvar_path+"%s_%s.png" % (str(id), suffix) ])
            except Exception, e:
                print "Why did montage fail?"
                raise e
                
        else:
            # Just make the lightcurve.
            
            plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                            timecolor=True, 
                            name = "%s:  UKvar %s (%s)" %
                            (str(s), str(id), suffix),
                            outfile=ukvar_path+"%s_%s.png" % 
                            (str(id), suffix))

        print "Completed UKvar %s" % str(id)

# And! This is a pure find-and-replace clone of `gen_ukvar_all()`! +some.
def gen_ukvar_all_jjh(start=0, stop=len(ukvar)):
    """ 
    Creates all the UKvar JJH plots in one shot.

    Uses the UKvar ID as the primary identifier; lists info
    in the filename distinguishing auto/strict/subj, plus per/nonper
    I'm thinking: 'a' for autovar, 't' for strict, 'j' for subj,
    'p' for periodic, 'n' for nonperiodic. Each dude gets two letters.

    The glued plots only consist of (a) colored-by-time and 
    (b) colored-by-phase. No periodograms here, go see the lightcurves
    for that.
    
    if periodic:
        do the gluedvars stuff
    else:
        just a normal lightcurve!

    """

    for s, id, i in zip(ukvar.SOURCEID, ukvar.UKvar_ID, 
                        range(len(ukvar)))[start:stop]:

        # Each plot gets a suffix: ('a'|'t'|'j')+('p'|'n')
        
        suffix = suffix_generator(ukvar, i)

        # Periodics first

        #        if ukvar.periodic[i] == 1:
        if False: # uncomment the above line when jjh_phase is functional.
            
            # Dig up the best period for this dude! 3 main cases.

            if ukvar.autovar[i] == 1:
                if s in autovars_true_periods.SOURCEID:
                    t = autovars_true_periods
                elif s in autovars_true_periods_s1.SOURCEID:
                    t = autovars_true_periods_s1
                else:
                    raise Exception("Something weird happened!")
            else:
                t = conf_subj_periodics
                
            best_period = t.best_period[t.SOURCEID == s][0]

            # Let's make 2 plots. LC and folded. Save em into a place.
            # print out the names as ID_fs_lc.png
            plot3.jjh(data, s, color_slope=True, 
                      date_offset=54034,
            #                      timecolor=True,
                      name = "%s:  UKvar %s (%s)" %
                      (str(s), str(id), suffix),
                      outfile=jjh_path+"%s_%s_lc.png" %
                      (str(id), suffix))

            # ID_fs_phase.png
            plot3.jjh_phase(data, s, timecolor='time', color_slope=True,
                            date_offset=54034,
                            period=best_period, 
                            name = "%s:  UKvar %s (%s)" %
                            (str(s), str(id), suffix),
                            outfile=jjh_path+"%s_%s_phase.png" % 
                            (str(id), suffix))


# now glue em together!
                
            try:
                call(["montage","-mode", "concatenate", "-tile", "2x", 
                      jjh_path+"%s_%s*.png" % (str(id), suffix), 
                      jjh_path_g+"%s_%s.png" % (str(id), suffix) ])
            except Exception, e:
                print "Why did montage fail?"
                raise e
                
        else:
            # Just make the lightcurve.
            
            plot3.jjh(data, s, color_slope=True, 
                      date_offset=54034,
            #                      timecolor=True, 
                      name = "%s:  UKvar %s (%s)" %
                      (str(s), str(id), suffix),
                      outfile=jjh_path_g+"%s_%s.png" % 
                      (str(id), suffix))

        print "Completed jjh: UKvar %s" % str(id)
        
        
def gen_lowvar_periodic_plots(start=0, stop=len(low_strict_periodics)):
    """
    Creates all the lowvar-strict plots in one shot.

    """
    
    counter = 1
    c_max = len(low_strict_periodics)

#    tables_of_periodics = [autovars_true_periods, autovars_true_periods_s1]

    print 'lol'
#    for t in tables_of_periodics:
#    print 'lol2'
        # first, the s123 periodics (more than 95% of them)
    for s in low_strict_periodics.SOURCEID[start:]:
        # If this is a strict autovar, we give it special stuff.
#        if s not in hivar.SOURCEID: continue
        # Let's make 3 plots. LC, folded, and pgram. Save em all into a place.
        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True, name=str(s),
                        outfile=lowvar_per_path+"%s_lc.png"%str(s))
        
        
        plot3.graded_phase(data, s, timecolor='time', 
                           name=str(s),
                           period=low_strict_periodics.best_period[
                low_strict_periodics.SOURCEID==s], 
                           color_slope=True, 
                           outfile=lowvar_per_path+"%s_phase.png"%str(s))
        
        try:
            plot3.lsp_power(data, s, 
                            outfile=lowvar_per_path+"%s_pgram.png"%str(s))
        except Exception, e:
            print "periodogram failed for %s" % str(s)
            print e
            
            
        # now glue em together!
        call(["montage","-mode", "concatenate", "-tile", "2x", 
              lowvar_per_path+"%s_*.png" % str(s), 
              lowvar_per_path_g+"%s-glued.png" % str(s) ])
        
        
        print "Completed plot %d of %d" % (counter, c_max)
        counter += 1
        
    return

def gen_lowvar_nonper_lc(start=0):
    """ Makes lightcurves for nonperiodic lowvars. """

    counter = 1
    c_max = len(low_strict_nonpers)

    for s in low_strict_nonpers.SOURCEID[start:]:

#        if s not in hivar.SOURCEID: continue
        # If this is a strict autovar, we give it special stuff.
#        if s in autovars_strict.SOURCEID:
#            flag = "s_"
#        else:
#            flag = ""

        plot3.graded_lc(data, s, abridged=True, color_slope=True, 
                        timecolor=True, name=str(s),
                        outfile=lowvar_path+"%s_lc.png"%str(s))

        print "Completed plot %d of %d" % (counter, c_max)
        counter += 1

    return



