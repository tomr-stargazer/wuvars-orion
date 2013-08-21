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
      Class from Megeath : string

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
    addc('Class (from Megeath et al. 2012)', megeath2012_by_ukvar.Class)

    # This writing convention is not sustainable.

    clobber_table_write(table,output_directory+"Table_1.txt", type='ascii')
    clobber_table_write(table,output_directory+"Table_1.tbl", type='ipac')
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

def t_table2_variability_periods_periodics_bymegeathclass():
    """
    Generates Table 2, which comes in three pieces.

    Note that we're only using periodic stars here!

    TODO: add in flags for whether a given star has valid
          J, H, or K data, respectively

    Current columns:
      Delta-J, H, K: three floats
      Delta-J-H, J-K, H-K: three floats
      Color slopes (JH, HK, JHK): three floats
      Stetson : one float
      Stetson_choice : one string
      Period : one float
      
    """

    table = atpy.Table()
    table.table_name = "Table 2"

    addc = table.add_column

    periodics = ukvar_spread.where(ukvar_spread.periodic != 0)
    periodic_periods = ukvar_periods[ukvar_spread.periodic != 0]
    megeath_by_periodics = megeath2012_by_ukvar.where(ukvar_spread.periodic != 0)

    # Do some stuff where we blank out color slopes that are no good
    jhk_slope_column = periodics.jhk_slope
    jhk_slope_column[~np.in1d(periodics.SOURCEID, jhk_filled.SOURCEID)] = np.nan

    jjh_slope_column = periodics.jjh_slope
    jjh_slope_column[~np.in1d(periodics.SOURCEID, jh_filled.SOURCEID)] = np.nan

    khk_slope_column = periodics.khk_slope
    khk_slope_column[~np.in1d(periodics.SOURCEID, hk_filled.SOURCEID)] = np.nan

    addc('UKvar ID', periodics.UKvar_ID)
    addc('J mag range (robust)', periodics.j_ranger)
    addc('H mag range (robust)', periodics.h_ranger)
    addc('K mag range (robust)', periodics.k_ranger)
    addc('J-H range (robust)', periodics.jmh_ranger)
    addc('H-K range (robust)', periodics.hmk_ranger)
    addc('(J-H), (H-K) color slope', jhk_slope_column)
    addc('J, (J-H) color slope', jjh_slope_column)
    addc('K, (H-K) color slope', khk_slope_column)
    addc('Stetson Variability Index', periodics.Stetson)
    addc('Bands used to compute Stetson', periodics.Stetson_choice)
    addc('Best-fit period', periodic_periods)

    # Now split it into three pieces and compute medians!
    
    t2_proto = table.where((megeath_by_periodics.Class == 'P') |
                           (megeath_by_periodics.Class == 'FP')|
                           (megeath_by_periodics.Class == 'RP'))

    t2_disks = table.where(megeath_by_periodics.Class == 'D')

    t2_nomegeath = table.where(megeath_by_periodics.Class == 'na')

    assert len(t2_proto) + len(t2_disks) + len(t2_nomegeath) == len(table), \
           "Tables don't add up to the right length!"

    clobber_table_write(t2_proto, output_directory+"Table_2a.txt", type='ascii')
    clobber_table_write(t2_disks, output_directory+"Table_2b.txt", type='ascii')
    clobber_table_write(t2_nomegeath, output_directory+"Table_2c.txt", type='ascii')

    
         
