"""
Inserts UKvar #1227 into ukvar_spread.

This is a one-off script to insert a single row into ukvar_spread. 
It's a clone of ukvar_1226_inserter_oneoff.py.

I'll tweak things as necessary.

"""

import os
import numpy as np

import atpy

from official_star_counter import subjectives
#from simbad_namer import simbad_namer

ukvar_spread = atpy.Table(
    os.path.expanduser(
        "~/Dropbox/Bo_Tom/aux_catalogs/UKvar_spreadsheet_withSIMBADnames_w1226_minusEasties_renamedOldONCvarColumn.fits"))

# We're gonna take ukvar_spread, a new "table" with just one row corresponding 
# to ukvar #1227, custom tailored with the right columns, and APPEND them!

# ID of UKvar 1227
uk1227_id = 44199508512491

uk1227 = subjectives.where(subjectives.SOURCEID == uk1227_id)

# now make uk1227 conform to ukvar_spread's 
unwanted_columns = [x for x in uk1227.columns.keys 
                    if (x not in ukvar_spread.columns.keys)]

print unwanted_columns

uk1227.remove_columns(unwanted_columns)

wanted_columns = [x for x in ukvar_spread.columns.keys 
                    if (x not in uk1227.columns.keys)]

print wanted_columns

missing_cols = ['autovar',
                'strict',
                'periodic',
                'old_ONCvar_ID',
                'SIMBAD_name',
                'clone',
                'UKvar_ID']

missing_vals =  [0., # not automatic
                 0., # not strict
                 0., # not periodic! (although it technically is because EB, but we didn't find it as such.)
                 -1, # has no "old" ONCvar ID -- only this and 1226 have this situation
                 '2MASS J05351214-0531388', # simbad_namer(uk1227)[0],
                 0, # not a clone! I hope!
                 1227] # 1226 existing UKvars.

missing_types = ['>f8', '>f8', '>f8', '>i8', '|S29', '>i8', '>i8']

for (column, value, dtype) in zip(missing_cols, missing_vals, missing_types):
    uk1227.add_column(column, np.array([value]), dtype=dtype)

for column in ukvar_spread.columns.keys:
    if ukvar_spread[column].dtype != uk1227[column].dtype:
        print (column, ": ", ukvar_spread[column].dtype, 
               uk1227[column].dtype)

# now let's do the appending

print ukvar_spread.shape
print uk1227.shape

ukvar_spread_w1227 = ukvar_spread.where(ukvar_spread.SOURCEID > 0)
ukvar_spread_w1227.append(uk1227)

# don't write anything till I'm ready!
assert 1==2

ukvar_spread_w1227.write(
    os.path.expanduser(
        "~/Dropbox/Bo_Tom/aux_catalogs/UKvar_spreadsheet_withSIMBADnames_w1226_minusEasties_renamedOldONCvarColumn_w1227.fits"))

