"""
Inserts UKvar #1226 into ukvar_spread.

This is a one-off script to insert a single row into ukvar_spread.

"""

import numpy as np

import atpy

from official_star_counter import low_periodics
from simbad_namer import simbad_namer

ukvar_spread = atpy.Table("/home/tom/Dropbox/Bo_Tom/aux_catalogs/UKvar_spreadsheet_withSIMBADnames.fits")

# We're gonna take ukvar_spread, a new "table" with just one row corresponding 
# to ukvar #1226, custom tailored with the right columns, and APPEND them!

# ID of UKvar 1226
uk1226_id = 44199508514050

uk1226 = low_periodics.where(low_periodics.SOURCEID == uk1226_id)

# now make uk1226 conform to ukvar_spread's 
unwanted_columns = [x for x in uk1226.columns.keys 
                    if (x not in ukvar_spread.columns.keys)]

print unwanted_columns

uk1226.remove_columns(unwanted_columns)

wanted_columns = [x for x in ukvar_spread.columns.keys 
                    if (x not in uk1226.columns.keys)]

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
                 simbad_namer(uk1226)[0], # 'V* V2033 Ori'
                 0, # not a clone! I hope!
                 1226] # 1225 existing UKvars.

#missing_types = [None, None, None, None, '|S29', None, None]

# table.add_column(name (str), data (array))
#uk1226.add_column
for (column, value) in zip(missing_cols, missing_vals):
    uk1226.add_column(column, np.array([value]))

for column in ukvar_spread.columns.keys:
    if ukvar_spread[column].dtype.type != uk1226[column].dtype.type:
        print (column, ": ", ukvar_spread[column].dtype.type, 
               uk1226[column].dtype.type)

# now let's do the appending

print ukvar_spread.shape
print uk1226.shape

ukvar_spread_w1226 = ukvar_spread.where(ukvar_spread.SOURCEID > 0)
ukvar_spread_w1226.append(uk1226)
