"""
Creates the 42-column ukvar_mated table (1226-star version).

This is the output of tablemate_script.UKvars_match(), with four
columns appended from ukvar_spread_w1226.

Update: now it also removes the "easties" (UKvar 1200-1225 minus 1203,1204)
by default, since tablemate_script implicitly does that.

Second update: Now we add in ONCvar 1227.

"""

from __future__ import division
import os

import numpy as np

from tablemate_script import UKvars_match, Rice_UKvars

dpath = os.path.expanduser("~/Dropbox/Bo_Tom/aux_catalogs/")


#create it
ukvar_spread = Rice_UKvars.data
mated_ukvar = UKvars_match()

missing_colnames = ['WFCAM_SOURCEID', 'RA', 'DEC', 'SIMBAD_name']
missing_colnames.reverse()

missing_cols = ['SOURCEID', 'RA', 'DEC', 'SIMBAD_name']
missing_cols.reverse()

for (col, name) in zip(missing_cols, missing_colnames):
    mated_ukvar.add_column(name, ukvar_spread[col], 
                           after="Rice2013_UKvars_index") 

mated_ukvar.table_name = "Mated UKvar"

# Don't write the file if it doesn't conform to what we expect it to look like!
assert len(mated_ukvar) == 1203, "Mated UKvar does not have 1203 rows!"
assert len(mated_ukvar.columns) == 46, "Mated UKvar does not have 46 columns!"

mated_ukvar.write(dpath+"ukvar_matched_table_withSIMBAD_w1226_minusEasties_w1227_2014_04_07.fits")
