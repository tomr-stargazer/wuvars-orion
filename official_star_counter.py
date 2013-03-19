"""
This is a script (not a module) that counts different types of
stars in my dataset using a self-consistent, editable, referenceable 
set of filters.

Useful importable variable names:
==Global==
 `autovars_true`: all automatically detected variables
 `autovars_strict`: all pristine auto-variables (a subset of `autovars_true`)
==Periodics==
 `autovars_true_periodics`: subset of `autovars_true` who are periodic
 `autovars_true_periods`: same as above, but only when we need their periods
 `autovars_strict_periodics`: subset of `autovars_strict` who are periodic
 `autovars_strict_periods`: same as above, but only when we need their periods
==Non-periodic==
 `autovars_true_nonpers`: subset of `autovars_true` who are non-periodic
 `autovars_strict_nonpers`: subset of `autovars_strict` who are non-periodic

""" 

from __future__ import division

import numpy as np

import atpy

import periodic_selector as ps

def c_print(str):
    if __name__ == '__main__':
        print str
    else:
        pass
    return
    

#spread = atpy.Table("/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5_spread.fits")
spread = atpy.Table("/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5_spread_pstar.fits")

maxvars_spread_per = atpy.Table("/media/storage/Documents/Research/reu/ORION/DATA/maxvars_data_statsper.fits")
maxvars_s1_spread_per = atpy.Table("/media/storage/Documents/Research/reu/ORION/DATA/maxvars_data_s1_statsper.fits")

maxvars_pstar = atpy.Table("/media/storage/Documents/Research/reu/ORION/DATA/maxvars_pstar.fits")


# Number of detected sources in the dataset
c_print( "Number of detected sources in the dataset:" )
c_print( len(spread) )

# Stars with valid data (that could be considered candidates for inclusion)
# Criteria:
#  At least 50 observations (as measured by Stetson_N or just per band)
#  

minimum = spread.where((spread.N_j >= 50) |
                       (spread.N_k >= 50) |
                       (spread.N_h >= 50) )

c_print( "Number of stars that meet absolute minimum considerations for valid data:" )
c_print( "(i.e., have at least 50 recorded observations in at least one band)" )
c_print( len(minimum) )

# Automatic variables
# Criteria:
#  At least one band must meet all of the following:
#  -At least 50 detections, less than 125
#  -Brightness between limits (11<K<16, 11<H<16, 11<J<17)
#  -No error flags at all (i.e. N_"info" = 0; severe stuff gets clipped anyway) 
#  AND Stetson value >= 1.
#  -Small caveat: if Stetson value dominated by disqualified bands,
#   observed RMS in a good band must > noise.

sp = spread

maxvars = sp.where( (sp.Stetson > 1) & (
        (sp.N_j >= 50) |
        (sp.N_k >= 50) |
        (sp.N_h >= 50) ) )
c_print( "Maximum possible number of variables: %d" % len(maxvars) )


autovars_old = sp.where( 
    (sp.Stetson > 1) & ( (
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & # J
        (sp.N_j_info == 0) ) | (              # J
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16) & # H
        (sp.N_h_info == 0) ) | (              # H
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & # K
        (sp.N_k_info == 0) ) ) )              # K

autocandidates_old = sp.where( (
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & # J
        (sp.N_j_info == 0) ) | (              # J
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16) & # H
        (sp.N_h_info == 0) ) | (              # H
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & # K
        (sp.N_k_info == 0) ) )                # K

# "True" variability criterion has two cases:
# 1. All 3 bands are quality, and S > 1 (this is identical to CygOB7), or
# 2. 1 or 2 bands is quality and has reduced chisq > 1, and S > 1 just in case.

# "Quality" is as defined above.

# Constructing these as two separate arrays for ease of reading/editing.
# Case 1: all 3 bands are quality; S > 1. Note "&"s uniform throughout.
case1 = ( (sp.Stetson > 1) & (sp.pstar_median > 0.75) &
          (
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & 
        (sp.N_j_info == 0) 
        ) &
          (
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16) & 
        (sp.N_h_info == 0) 
        ) &
          (
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & 
        (sp.N_k_info == 0)
        ) )

# Case 2: at least one band quality and rchi^2 > 1; S > 1. Note mixed "&"s 
# and "|"s, as well as another layer of parentheses around the complex of "|"
# criteria.
case2 = ( ((sp.Stetson > 1) & (sp.pstar_median > 0.75)) & (
          (
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & 
        (sp.N_j_info == 0) & (sp.j_rchi2 > 1) 
        ) |
          (
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16) & 
        (sp.N_h_info == 0) & (sp.h_rchi2 > 1) 
        ) |
          (
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & 
        (sp.N_k_info == 0) & (sp.k_rchi2 > 1) 
        ) ) )

autovars_true = sp.where( case1 | case2 )

autovars_strict = sp.where( case1 )


# Now, to count how many stars have quality that meets "autovars_true".

# Constructing these as two separate arrays for ease of reading/editing.
# Case 1: all 3 bands are quality. Note "&"s uniform throughout.
cand_case1 = ( (sp.pstar_median > 0.75) & ( 
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & 
        (sp.N_j_info == 0) 
        ) &
          (
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16) & 
        (sp.N_h_info == 0) 
        ) &
          (
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & 
        (sp.N_k_info == 0)
        ) )

# Case 2: at least one band quality. Note mixed "&"s and "|"s, 
# as well as another layer of parentheses around the complex of "|" criteria.
cand_case2 = ( (sp.pstar_median > 0.75) & (
    (
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & 
        (sp.N_j_info == 0) 
        ) |
    (
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16) & 
        (sp.N_h_info == 0) 
        ) |
    (
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & 
        (sp.N_k_info == 0) 
        ) ) )


autocan_true = sp.where( cand_case1 | cand_case2 )

autocan_strict = sp.where( cand_case1 )

c_print( "Number of stars automatically classed as variables: %d" % len(autovars_true) )
c_print( "Number of stars that have the data quality for auto-classification: %d" % len(autocan_true) )

subjectives = maxvars.where( ~np.in1d(maxvars.SOURCEID, autovars_true.SOURCEID))

old_subjectives = atpy.Table("/home/tom/reu/ORION/DATA/old_subjectives.fits")

new_subjectives = subjectives.where( ~np.in1d(subjectives.SOURCEID, old_subjectives.SOURCEID))

c_print( "" )
c_print( "Number of probably-variable stars requiring subjective verification due to imperfect data quality: %d" % len(subjectives) )

c_print( "Number of new subjectives: %d" % len(new_subjectives) )

# Now let's count stars that meet our strict criteria in ALL 3 bands

c_print( "" )

c_print( "Number of STRICT autovariables: %d" % len(autovars_strict) )
c_print( "Number of STRICT autocandidates: %d" % len(autocan_strict) )

c_print( "" )

c_print( " Q: Statistically, what fraction of our stars are variables?" )
c_print( " A: %.2f%s, drawn from the tightest-controlled sample;" % (len(autovars_strict)/len(autocan_strict) * 100, r"%") )
c_print( "    %.2f%s, drawn from a looser sample." % (len(autovars_true)/len(autocan_true) * 100, r"%") )

# Now for periodicity analysis, which relies on periodic_selector

# THIS WON'T WORK, we have to bring in the maxvars_data_statsper which has been period-analyzed, and then do cuts of it that correspond to autovars, etc
#autovars_true_periodic = ps.periodic_selector(autovars_true)
#autovars_strict_periodic = ps.periodic_selector(autovars_true)

periodics_s123 = ps.periodic_selector(maxvars_spread_per)
periodics_s1 = ps.periodic_selector(maxvars_s1_spread_per)

maxvars_periodics = maxvars.where( 
    np.in1d(maxvars.SOURCEID, periodics_s123.SOURCEID) |
    np.in1d(maxvars.SOURCEID, periodics_s1.SOURCEID) )


autovars_true_periodics = autovars_true.where( 
    np.in1d(autovars_true.SOURCEID, periodics_s123.SOURCEID) |
    np.in1d(autovars_true.SOURCEID, periodics_s1.SOURCEID) )

autovars_strict_periodics = autovars_strict.where(
    np.in1d(autovars_strict.SOURCEID, periodics_s123.SOURCEID) |
    np.in1d(autovars_strict.SOURCEID, periodics_s1.SOURCEID) )

c_print( "" )
c_print( "Number of possible variables with detected periods: %d" % len(maxvars_periodics) )
c_print( "Number of autovariables that are periodic: %d" % len(autovars_true_periodics) )
c_print( "Number of STRICT autovariables that are periodic: %d" % len(autovars_strict_periodics) )
c_print( "Number of possible periodic variables requiring subjective validation: %d" % (len(maxvars_periodics) - len(autovars_true_periodics)) )
c_print( "" )


c_print( " Q: Statistically, what fraction of our variables are periodic?" )
c_print( " A: %.2f%s, drawn from the tightest-controlled sample;" % (len(autovars_strict_periodics)/len(autovars_strict) * 100, r"%") )
c_print( "    %.2f%s, drawn from a looser sample." % (len(autovars_true_periodics)/len(autovars_true) * 100, r"%") )

c_print( "" )
c_print( " Q: What fraction of stars in this dataset are periodic variables?" )
c_print( " A: %.2f%s, drawn from the tightest-controlled sample;" % (len(autovars_strict_periodics)/len(autocan_strict) * 100, r"%") )
c_print( "    %.2f%s, drawn from a looser sample." % (len(autovars_true_periodics)/len(autocan_true) * 100, r"%") )

# The following is only suitable for almost-but-not-quite 
# accurate histogram analysis (because it ditches the s1-only periodocs)

# intersection of periodics_s123 and maxvars_periodics
maxvars_periods = periodics_s123.where( 
    np.in1d(periodics_s123.SOURCEID, maxvars_periodics.SOURCEID))

# etc
autovars_true_periods = ps.best_period(periodics_s123.where( 
    np.in1d(periodics_s123.SOURCEID, autovars_true_periodics.SOURCEID)))

autovars_strict_periods = ps.best_period(periodics_s123.where( 
    np.in1d(periodics_s123.SOURCEID, autovars_strict_periodics.SOURCEID)))

autovars_true_periods_s1 = ps.best_period(periodics_s1.where( 
    np.in1d(periodics_s1.SOURCEID, autovars_true_periodics.SOURCEID) &
    ~np.in1d(periodics_s1.SOURCEID, autovars_true_periods.SOURCEID)))

#print "hey look i'm here"

## The following creates spreadsheets of nonvariables, as an official reference,
# such that I don't botch anything down the line.

# Nonperiodic autovariables
autovars_true_nonpers = autovars_true.where(
    ~np.in1d(autovars_true.SOURCEID, autovars_true_periodics.SOURCEID))

autovars_strict_nonpers = autovars_strict.where(
    ~np.in1d(autovars_strict.SOURCEID, autovars_strict_periodics.SOURCEID))


### Here we're gonna sort the NEW subjectives into two categories:
# Periodic, and Nonperiodic. This will be via a comparison with the 
# `maxvars_periodics` table.

new_subjectives_nonpers = new_subjectives.where(
    ~np.in1d(new_subjectives.SOURCEID, maxvars_periodics.SOURCEID))

new_subjectives_per_s123 = periodics_s123.where(
    np.in1d(periodics_s123.SOURCEID, new_subjectives.SOURCEID))

# those that are in s1 but NOT in s123
new_subjectives_per_s1 = periodics_s1.where(
    np.in1d(periodics_s1.SOURCEID, new_subjectives.SOURCEID) & 
    ~np.in1d(periodics_s1.SOURCEID, periodics_s123.SOURCEID))

#print len(new_subjectives_nonpers)
#print len(new_subjectives_per_s123)
#print len(new_subjectives_per_s1)
#print "those are things. End."

if len(new_subjectives_per_s1) == 0:
    new_subjectives_per = ps.best_period(new_subjectives_per_s123)
#    print "assigned best periods"


##### Now let's talk about LOW VARIABLES.

# Low variables.
low_maxvars = sp.where( (sp.Stetson <= 1.0) & (sp.Stetson > 0.55) &(
        (sp.N_j >= 50) |
        (sp.N_k >= 50) |
        (sp.N_h >= 50) ) )
c_print( "Maximum possible number of LOW-variables: %d" % len(low_maxvars) )

# Low variability criterion has two cases:
# 1. All 3 bands are quality, and 1.0 > S > 0.55, or
# 2. 1 or 2 bands is quality and has reduced chisq > 1, and 1 > S > 0.55 still.

# "Quality" is as defined above.

# Constructing these as two separate arrays for ease of reading/editing.
# Case 1: all 3 bands are quality; S > 1. Note "&"s uniform throughout.
low_case1 = ( (sp.Stetson > 0.55) & (sp.Stetson <= 1.0) &
              (sp.pstar_median > 0.75) &
              (
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & 
        (sp.N_j_info == 0) 
        ) &
              (
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16) & 
        (sp.N_h_info == 0) 
        ) &
              (
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & 
        (sp.N_k_info == 0)
        ) )

# Case 2: at least one band quality and rchi^2 > 1; S > 1. Note mixed "&"s 
# and "|"s, as well as another layer of parentheses around the complex of "|"
# criteria.
low_case2 = ( ((sp.Stetson > 0.55) & (sp.Stetson <= 1.0) & 
               (sp.pstar_median > 0.75)) & (
        (
            (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
            (sp.j_mean > 11) & (sp.j_mean < 17) & 
            (sp.N_j_info == 0) & (sp.j_rchi2 > 1) 
            ) |
        (
            (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
            (sp.h_mean > 11) & (sp.h_mean < 16) & 
            (sp.N_h_info == 0) & (sp.h_rchi2 > 1) 
            ) |
        (
            (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
            (sp.k_mean > 11) & (sp.k_mean < 16) & 
            (sp.N_k_info == 0) & (sp.k_rchi2 > 1) 
            ) ) ) 

low_autovars = sp.where( low_case1 | low_case2 )

low_autovars_strict = sp.where( low_case1 )


# Now, to count how many stars have quality that meets "autovars_true".
# Done above. See "autocan_true" and "autocan_strict".

c_print( "Number of stars automatically classed as LOW variables: %d" % len(low_autovars) )
c_print( "Number of stars that have the data quality for auto-classification: %d" % len(autocan_true) )


low_maxvars_spread = atpy.Table("/media/storage/Documents/Research/reu/ORION/DATA/low_maxvars_data_spread.fits")
low_periodics = ps.best_period(ps.periodic_selector(low_maxvars_spread))

low_strict_periodics = low_periodics.where(
    np.in1d(low_periodics.SOURCEID, low_autovars_strict.SOURCEID))

low_strict_nonpers = low_autovars_strict.where(
    ~np.in1d(low_autovars_strict.SOURCEID, low_strict_periodics.SOURCEID))


c_print( "Number of LOW strict variables: %d" % len(low_autovars_strict) )
c_print( "Number of LOW periodic-strict stars: %d" % len(low_strict_periodics))
