"""
This is a script to create a master variable list from our study
that can be matched against other catalogs.

Basically, it glues together the autovar and subjvar tables,
but in a controlled and intelligent way.
"""

import numpy as np

import atpy

from official_star_counter import *

from montage_script import conf_subj_periodics, conf_subj_nonpers

spread = atpy.Table("/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5_spread_pstar.fits")

# Let's start with autovars_true, and add the three columns to it.
# These three columns should be: Autovar? Strict? Periodic?
# Then we fill in these columns by comparing to
# (a) itself, which is all TRUE, (b) autovars_strict, and (c) autovars_true_periodics .

# the following is an inelegant way of making a copy
autovars = autovars_true.where( autovars_true.SOURCEID > 0)

autovars.add_column('autovar', np.ones(len(autovars)))
autovars.add_column('strict', np.zeros(len(autovars)))
autovars.add_column('periodic', np.zeros(len(autovars)))

# fill in strict
autovars.strict[ 
    np.in1d(autovars.SOURCEID, autovars_strict.SOURCEID) ] = 1

# fill in periodic
autovars.periodic[ 
    np.in1d(autovars.SOURCEID, autovars_true_periodics.SOURCEID) ] = 1

# OKAY, now let's do the confirmed subj_periodics and subj_nonpers.
# We need them to fit into the same column structure, so I may do a thing
# where I extract the rows of `spread` that correspond to entries in 
# either subj_p and subj_np.

# `conf_subj_nonpers` and `conf_subj_periodics` are created in montage_script
# and are UP TO DATE.

subjvars = spread.where( 
    np.in1d(spread.SOURCEID, conf_subj_nonpers.SOURCEID) |
    np.in1d(spread.SOURCEID, conf_subj_periodics.SOURCEID) )

print len(subjvars)

subjvars.add_column('autovar', np.zeros(len(subjvars)))
subjvars.add_column('strict', np.zeros(len(subjvars)))
subjvars.add_column('periodic', np.zeros(len(subjvars)))

subjvars.periodic[
    np.in1d(subjvars.SOURCEID, conf_subj_periodics.SOURCEID) ] = 1

gluedvars = autovars.where(autovars.SOURCEID > 0)
gluedvars.append( subjvars )

