"""
This is a script for generating TABLES for the Orion WFCAM time-series paper.

Guide to variable names:

 =====PERIODICS======
 Currently, we're using 
 `conf_subj_periodics` for subjective periodics,
 `autovars_true_periodics` for the superset of automatically detected and pristine/strict periodic variables, and `autovars_true_periods` when we need their `best_period`s (but NEVER otherwise, for strange reasons)
 `autovars_strict_periodics` for pristine/strict variables, and `autovars_strict_periods` when we need their `best_period`s (but NEVER otherwise, for strange reasons)
 =====NON-PERIODICS======
 `conf_subj_nonpers` for subjective nonperiodics
 `autovars_true_nonpers` for the superset of automatically detected and pristine/strict nonperiodic variables
 `autovars_strict_nonpers` for pristine/strict nonperiodic variables

 =====GLOBAL======
 `autovars_true` for all automatically detected variables (incl. pristines)
 `autovars_strict` for all pristine variables
 `maxvars`

"""

import os
# All of these imports are meant to mirror those from figure_maker.

from official_star_counter import *
from color_slope_filtering import (jhk_empty, jhk_filled, jh_empty, jh_filled,
                                   hk_empty, hk_filled)
from tablemate_comparisons import (mated_ukvar, ukvar_spread, 
                                   ukvar_periods, source_period_digger)
from tablemate_script import (Megeath2012, Megeath_P, Megeath_D)
from orion_tablemate import index_secondary_by_primary

from montage_script import conf_subj_periodics, conf_subj_nonpers

output_directory = "/home/tom/Dropbox/Bo_Tom/paper/publication_tables/"

# Let's grab IRAC colors from Megeath.
megeath2012_by_ukvar = index_secondary_by_primary(mated_ukvar, Megeath2012)

def clobber_table_write(table, filename, **kwargs):
    """ Writes a table, even if it has to clobber an older one. """

    try:
        table.write(filename, **kwargs)
    except Exception, e: 
        print e
        print "Overwriting file."
        os.remove(filename)
        table.write(filename, **kwargs)
        
def t_table1_radec_xref_jhk_irac():
    """
    Generates Table 1.

    Current columns:
      UKvar ID : int  ## note: will likely be migrated to "ONCvar ID" in paper
      RA : float, degrees
      DEC : float, degrees # note: we could probably have an optional sexg. format for these
      X-ref : string # Using SIMBAD names for now.
      Median J, H, K, with error bars : six floats
      IRAC colors from Megeath, and errors : eight floats

    Returns
    -------
    table : atpy.Table
        Table 1.

    """

    table = atpy.Table()
    table.table_name = "Table 1"

    addc = table.add_column

    addc('UKvar ID', ukvar_spread.UKvar_ID)
    addc('R.A. (deg)', np.degrees(ukvar_spread.RA))
    addc('Decl. (deg)', np.degrees(ukvar_spread.DEC))
    addc('SIMBAD Cross-reference', ukvar_spread.SIMBAD_name)
    addc('Median J mag', ukvar_spread.j_median)
    addc('Median J mag error', ukvar_spread.j_err_median)
    addc('Median H mag', ukvar_spread.h_median)
    addc('Median H mag error', ukvar_spread.h_err_median)
    addc('Median K mag', ukvar_spread.k_median)
    addc('Median K mag error', ukvar_spread.k_err_median)
    addc('Spitzer [3.6] mag', megeath2012_by_ukvar['3.6mag'])
    addc('Spitzer [3.6] mag error', megeath2012_by_ukvar['e_3.6mag'])
    addc('Spitzer [4.5] mag', megeath2012_by_ukvar['4.5mag'])
    addc('Spitzer [4.5] mag error', megeath2012_by_ukvar['e_4.5mag'])
    addc('Spitzer [5.8] mag', megeath2012_by_ukvar['5.8mag'])
    addc('Spitzer [5.8] mag error', megeath2012_by_ukvar['e_5.8mag'])
    addc('Spitzer [8.0] mag', megeath2012_by_ukvar['8.0mag'])
    addc('Spitzer [8.0] mag error', megeath2012_by_ukvar['e_8.0mag'])

    # This writing convention is not sustainable.

    clobber_table_write(table,output_directory+"Table_1.txt", type='ascii')
    # try:
    #     table.write()
    # except Exception, e: 
    #     print e
    #     print "Overwriting file."
    #     os.remove(output_directory+"Table_1.txt")
    #     table.write(output_directory+"Table_1.txt", type='ascii')
        
    clobber_table_write(table, output_directory+"Table_1.fits")

    return table


# for table 2, or some other table:
"""
    addc('Observed J RMS', ukvar_spread.j_rms)
    addc('Observed H RMS', ukvar_spread.h_rms)
    addc('Observed K RMS', ukvar_spread.k_rms)
    addc('Outlier-proof J range', ukvar_spread.j_ranger)    
    addc('Outlier-proof H range', ukvar_spread.h_ranger)
    addc('Outlier-proof K range', ukvar_spread.k_ranger)
"""
