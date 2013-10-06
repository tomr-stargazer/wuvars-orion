"""
This is a oneoff script whose purpose is to rename the ONCvar_ID column
to old_ONCvar_ID in any relevant existing tables.

"""

import os

import atpy

# use atpy.Table.rename_column( `old_name`, `new_name` )


def renamer(table):

    if 'ONCvar_ID' in table.columns.keys and 'UKvar_ID' in table.columns.keys:
        table.rename_column('ONCvar_ID', 'old_ONCvar_ID')
        return table

    else:
        raise ValueError("Input table needs both an ONCvar_ID column and a UKvar_ID column!")


    
if __name__ == '__main__':

    dropbox_bo_aux_catalogs = os.path.expanduser("~/Dropbox/Bo_Tom/aux_catalogs/")
    
    ukvar_spread = atpy.Table(dropbox_bo_aux_catalogs+"UKvar_spreadsheet_withSIMBADnames_w1226_minusEasties.fits")

    new_ukvar_spread = renamer(ukvar_spread)

    new_ukvar_spread.write( dropbox_bo_aux_catalogs+"UKvar_spreadsheet_withSIMBADnames_w1226_minusEasties_renamedOldONCvarColumn.fits")

    
