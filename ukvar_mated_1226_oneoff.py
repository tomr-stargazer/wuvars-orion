"""
Creates the 42-column ukvar_mated table (1226-star version).

This is the output of tablemate_script.UKvars_match(), with four
columns appended from ukvar_spread_w1226.

"""

import numpy as np

import atpy

from tablemate_script import UKvars_match, Rice_UKvars


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

#mated_ukvar.add_column('DEC', ukvar_spread.DEC, 
#                       after="Rice2013_UKvars_index")
#mated_ukvar.add_column('RA', ukvar_spread.RA, 
#                       after="Rice2013_UKvars_index")
#mated_ukvar.add_column('WFCAM_SOURCEID', ukvar_spread.WFCAM_SOURCEID, 
#                       after="Rice2013_UKvars_index")

print mated_ukvar.columns
print mated_ukvar.shape
