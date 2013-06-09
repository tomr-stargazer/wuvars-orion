"""
Creates the 42-column ukvar_mated table (1226-star version).

This is the output of tablemate_script.UKvars_match(), with four
columns appended from ukvar_spread_w1226.

"""

import numpy as np

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


mated_ukvar.write("/home/tom/Dropbox/Bo_Tom/aux_catalogs/ukvar_matched_table_withSIMBAD_w1226_2013_6_09.fits")