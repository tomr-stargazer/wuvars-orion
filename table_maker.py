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

# All of these imports are meant to mirror those from figure_maker.

from official_star_counter import *
from color_slope_filtering import (jhk_empty, jhk_filled, jh_empty, jh_filled,
                                   hk_empty, hk_filled)
from tablemate_comparisons import (mated_ukvar, ukvar_spread, 
                                   ukvar_periods, source_period_digger)
from tablemate_script import (Megeath2012, Megeath_P, Megeath_D)

from montage_script import conf_subj_periodics, conf_subj_nonpers

output_directory = "/home/tom/Dropbox/Bo_Tom/paper/publication_tables/"

# Let's grab IRAC colors from Megeath.
#ukvar_irac = atpy.Table('UKvar IRAC')

# Test case: 3.6um.
# Where there's a valid match, grab the Megeath data; else put nan.

irac1 = np.zeros(len(ukvar_spread))
irac1_e = np.zeros(len(ukvar_spread))

for i in range(len(mated_ukvar)):
    if mated_ukvar.Megeath2012_ID[i] != -1:
        irac1[i] = Megeath2012.data['3.6mag'][mated_ukvar.Megeath2012_index[i]]
    else:
        irac1[i] = np.nan

print irac1


def t_table1_radec_xref_jhk_rms_minmax_irac():
    """
    Generates Table 1.

    Current columns:
      UKvar ID : int  ## note: will likely be migrated to "ONCvar ID" in paper
      RA : float, degrees
      DEC : float, degrees # note: we could probably have an optional sexg. format for these
      X-ref : string # Using SIMBAD names for now.
      Median J, H, K, with error bars : six floats
      RMS J, H, K : three floats
      robust range J, H, K : three floats
      IRAC colors from Megeath, and errors : eight floats

    """

    table = atpy.Table()
    table.table_name = "Table 1"

    addc = table.add_column

    addc('UKvar ID', ukvar_spread.UKvar_ID)
    addc('R.A. (deg)', np.degrees(ukvar_spread.RA))
    addc('Decl. (deg)', np.degrees(ukvar_spread.DEC))
    addc('Cross-reference', ukvar_spread.SIMBAD_name)
    addc('Median J mag', ukvar_spread.j_median)
    addc('Median J mag error', ukvar_spread.j_err_median)
    addc('Median H mag', ukvar_spread.h_median)
    addc('Median H mag error', ukvar_spread.h_err_median)
    addc('Median K mag', ukvar_spread.k_median)
    addc('Median K mag error', ukvar_spread.k_err_median)
    addc('Observed J RMS', ukvar_spread.j_rms)
    addc('Observed H RMS', ukvar_spread.h_rms)
    addc('Observed K RMS', ukvar_spread.k_rms)
    addc('Outlier-proof J range', ukvar_spread.j_ranger)    
    addc('Outlier-proof H range', ukvar_spread.h_ranger)
    addc('Outlier-proof K range', ukvar_spread.k_ranger)

    # This writing convention is not sustainable.
    try:
        table.write(output_directory+"Table_1.txt", type='ascii')
    except Exception, e: print e
    try:
        table.write(output_directory+"Table_1.fits")
    except Exception, e: print e

      
