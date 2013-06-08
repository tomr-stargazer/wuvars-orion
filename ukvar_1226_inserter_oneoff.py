"""
Inserts UKvar #1226 into ukvar_spread.

This is a one-off script to insert a single row into ukvar_spread.

"""

import numpy as np

from official_star_counter import low_periodics

ukvar_spread = atpy.Table("/home/tom/Dropbox/Bo_Tom/aux_catalogs/UKvar_spreadsheet_withSIMBADnames.fits")

# We're gonna take ukvar_spread, a new "table" with just one row corresponding 
# to ukvar #1226, custom tailored with the right columns, and APPEND them!

# ID of UKvar 1226
uk1226_id = 44199508514050

