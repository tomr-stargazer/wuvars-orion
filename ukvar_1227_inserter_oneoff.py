"""
Inserts UKvar #1227 into ukvar_spread.

This is a one-off script to insert a single row into ukvar_spread. 
It does some fancy things to (a) make sure all the values are correct, 
especially the SIMBAD name; and (b) make sure the appending process goes 
properly.

I've noticed that sometimes, when I run this multiple times in pylab, 
it'll segfault. Just a note.

"""

import numpy as np

import atpy

from official_star_counter import low_periodics
from simbad_namer import simbad_namer

ukvar_spread = atpy.Table("/home/tom/Dropbox/Bo_Tom/aux_catalogs/UKvar_spreadsheet_withSIMBADnames.fits")

# We're gonna take ukvar_spread, a new "table" with just one row corresponding 
# to ukvar #1227, custom tailored with the right columns, and APPEND them!

# ID of UKvar 1227
uk1227_id = 44199508514050

uk1227 = low_periodics.where(low_periodics.SOURCEID == uk1227_id)

assert 1 == 2

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
                'ONCvar_ID',
                'SIMBAD_name',
                'clone',
                'UKvar_ID']

missing_vals =  [0., # not automatic
                 0., # not strict
                 1., # periodic!
                 -1, # not an ONCvar -- unique among UKvars
                 simbad_namer(uk1227)[0], # 'V* V2033 Ori'
                 0, # not a clone! I hope!
                 1227] # 1225 existing UKvars.

missing_types = ['>f8', '>f8', '>f8', '>i8', '|S29', '>i8', '>i8']

# table.add_column(name (str), data (array))
#uk1227.add_column


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

ukvar_spread_w1227.write("/home/tom/Dropbox/Bo_Tom/aux_catalogs/UKvar_spreadsheet_withSIMBADnames_w1227.fits")
