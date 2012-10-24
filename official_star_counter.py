"""
This is a script (not a module) that counts different types of
stars in my dataset using a self-consistent, editable, referenceable 
set of filters.

""" 

import numpy as np

import atpy

spread = atpy.Table("/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5_spread.fits")

# Number of detected sources in the dataset
print "Number of detected sources in the dataset:"
print len(spread)

# Stars with valid data (that could be considered candidates for inclusion)
# Criteria:
#  At least 50 observations (as measured by Stetson_N or just per band)
#  

minimum = spread.where(spread.Stetson_N > 50)
alt_minimum = spread.where((spread.N_j >= 50) |
                           (spread.N_k >= 50) |
                           (spread.N_h >= 50) )

print "Number of stars that meet absolute minimum considerations for valid data:"
print "(i.e., have at least 50 recorded observations in at least one band)"
print len(minimum)
print len(alt_minimum)


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
print "Maximum possible number of variables: %d" % len(maxvars)

jvars = sp.where(   
    (sp.Stetson > 1) & (
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & # J
        (sp.N_j_info == 0) ) )                # J

print "number of autovariables that have qualifying J bands: %d" % len(jvars)

hvars = sp.where(   
    (sp.Stetson > 1) & (
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 17) & # H
        (sp.N_h_info == 0) ) )                # H

print "number of autovariables that have qualifying H bands: %d" % len(hvars)

kvars = sp.where(   
    (sp.Stetson > 1) & (
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 17) & # K
        (sp.N_k_info == 0) ) )                # K

print "number of autovariables that have qualifying K bands: %d" % len(kvars)

print "Maximum number of autovariables: %d" % (len(jvars)+len(hvars)+len(kvars))

autovars = sp.where( 
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

# "True" variability criterion has two cases:
# 1. All 3 bands are quality, and S > 1 (this is identical to CygOB7), or
# 2. 1 or 2 bands is quality and has reduced chisq > 1, and S > 1 just in case.

# "Quality" is as defined above.

# Constructing these as two separate arrays for ease of reading/editing.
# Case 1: all 3 bands are quality; S > 1. Note "&"s uniform throughout.
case1 = ( (sp.Stetson > 1) &
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
case2 = ( (sp.Stetson > 1) & (
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

autocandidates = sp.where( (
        (sp.N_j >= 50) & (sp.N_j <= 125) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & # J
        (sp.N_j_info == 0) ) | (              # J
        (sp.N_h >= 50) & (sp.N_h <= 125) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16) & # H
        (sp.N_h_info == 0) ) | (              # H
        (sp.N_k >= 50) & (sp.N_k <= 125) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & # K
        (sp.N_k_info == 0) ) )                # K

# Now, to count how many stars have quality that meets "autovars_true".

# Constructing these as two separate arrays for ease of reading/editing.
# Case 1: all 3 bands are quality. Note "&"s uniform throughout.
cand_case1 = ( ( 
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
cand_case2 = ( 
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
        ) )


autocan_true = sp.where( cand_case1 | cand_case2 )


print "Number of automatically detected variables: %d" % len(autovars)
print "Number of stars that meet autoquality cuts: %d" % len(autocandidates)
print " "
print "Number of TRUE autovariables: %d" % len(autovars_true)
print "Number of TRUE autocandidates: %d" % len(autocan_true)
