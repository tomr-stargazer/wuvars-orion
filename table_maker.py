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

try:
    import coords
except ImportError:
    import astrolib.coords as coords

import astropy.io.ascii
import astropy.table

# All of these imports are meant to mirror those from figure_maker.
from official_star_counter import *
from color_slope_filtering import (jhk_empty, jhk_filled, jh_empty, jh_filled,
                                   hk_empty, hk_filled)
from tablemate_comparisons import (mated_ukvar, ukvar_spread, 
                                   ukvar_periods, source_period_digger)
from tablemate_script import (Megeath2012, Megeath_P, Megeath_D)
from orion_tablemate import index_secondary_by_primary

from montage_script import conf_subj_periodics, conf_subj_nonpers

dropbox_bo = os.path.expanduser("~/Dropbox/Bo_Tom/")
output_directory = dropbox_bo+"paper/publication_tables/"


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
      Data quality : int (0, 1, 2) corresponding to subjective/auto/strict
      Periodic : int (0, 1)
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
    addc('Data quality flag', ukvar_spread.autovar + ukvar_spread.strict)
    addc('Periodic flag', ukvar_spread.periodic)
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
    N_j, N_h, N_k : three integers
      Delta-J, H, K: three floats
      Delta-J-H, J-K, H-K: three floats
      Color slopes (JH, HK, JHK): three floats
      Stetson : one float
      Stetson_choice : one string
      Period : one float
      Data quality : int (0, 1, 2) corresponding to subjective/auto/strict
      
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
    addc('N_J', periodics.N_j)
    addc('N_H', periodics.N_h)
    addc('N_K', periodics.N_k)
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
    addc('Data quality flag', periodics.autovar + periodics.strict)

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

    return table

def t_table3_variability_nonperiodics_bymegeathclass():
    """
    Generates Table 3, which also comes in three pieces.

    Only non-periodic stars; has many of the same columns as Table 2.

    Current columns:
      N_j, N_h, N_k : three integers
      Delta-J, H, K: three floats
      Delta-J-H, J-K, H-K: three floats
      Color slopes (JH, HK, JHK): three floats
      Stetson : one float
      Stetson_choice : one string
      Data quality : int (0, 1, 2) corresponding to subjective/auto/strict

    """

    table = atpy.Table()
    table.table_name = "Table 3"

    addc = table.add_column

    nonperiodics = ukvar_spread.where(ukvar_spread.periodic == 0)
    megeath_by_nonperiodics = megeath2012_by_ukvar.where(ukvar_spread.periodic == 0)

    # Do some stuff where we blank out color slopes that are no good
    jhk_slope_column = nonperiodics.jhk_slope
    jhk_slope_column[~np.in1d(nonperiodics.SOURCEID, jhk_filled.SOURCEID)] = np.nan

    jjh_slope_column = nonperiodics.jjh_slope
    jjh_slope_column[~np.in1d(nonperiodics.SOURCEID, jh_filled.SOURCEID)] = np.nan

    khk_slope_column = nonperiodics.khk_slope
    khk_slope_column[~np.in1d(nonperiodics.SOURCEID, hk_filled.SOURCEID)] = np.nan

    addc('UKvar ID', nonperiodics.UKvar_ID)
    addc('N_J', nonperiodics.N_j)
    addc('N_H', nonperiodics.N_h)
    addc('N_K', nonperiodics.N_k)
    addc('J mag range (robust)', nonperiodics.j_ranger)
    addc('H mag range (robust)', nonperiodics.h_ranger)
    addc('K mag range (robust)', nonperiodics.k_ranger)
    addc('J-H range (robust)', nonperiodics.jmh_ranger)
    addc('H-K range (robust)', nonperiodics.hmk_ranger)
    addc('(J-H), (H-K) color slope', jhk_slope_column)
    addc('J, (J-H) color slope', jjh_slope_column)
    addc('K, (H-K) color slope', khk_slope_column)
    addc('Stetson Variability Index', nonperiodics.Stetson)
    addc('Bands used to compute Stetson', nonperiodics.Stetson_choice)
    addc('Data quality flag', nonperiodics.autovar + nonperiodics.strict)

    # Now split it into three pieces and compute medians!
    t3_proto = table.where((megeath_by_nonperiodics.Class == 'P') |
                           (megeath_by_nonperiodics.Class == 'FP')|
                           (megeath_by_nonperiodics.Class == 'RP'))

    t3_disks = table.where(megeath_by_nonperiodics.Class == 'D')

    t3_nomegeath = table.where(megeath_by_nonperiodics.Class == 'na')

    assert len(t3_proto) + len(t3_disks) + len(t3_nomegeath) == len(table), \
           "Tables don't add up to the right length!"

    clobber_table_write(t3_proto, output_directory+"Table_3a.txt", type='ascii')
    clobber_table_write(t3_disks, output_directory+"Table_3b.txt", type='ascii')
    clobber_table_write(t3_nomegeath, output_directory+"Table_3c.txt", type='ascii')

    return table
    
         
def t_table0_crossref():
    """
    Generates Table 'zero', which probably won't go in the print paper,
    but enumerates how our sources match up (positionally) against 
    18 different datasets from the published literature on the ONC.

    Yes, 18 different datasets. I'll have to make sure that the 
    document describing where they exactly came from is made available,
    so that my indexing system is clear.

    """
    
    table = mated_ukvar.where(mated_ukvar.WFCAM_SOURCEID > 0)
    table.table_name = "Table 0"

    clobber_table_write(table, output_directory+"Table_0.txt", type='ascii')
    clobber_table_write(table, output_directory+"Table_0.fits")

    return table

def join_columns_with_plusminus(value_column, error_column, precision=3):
    """
    Joins two data columns together with the LaTeX $\pm$ symbol.

    Outputs an array of strings, rather than an array of values, 
    so this is really only useful if you're going to write this as 
    a LaTeX table.

    Parameters
    ----------
    value_column : np.array
        A column of values (such as magnitudes, masses, etc).
    error_column : np.array
        The column of associated errors on those values.
    precision : int, optional
        The number of decimal places to keep in the value and error columns
        when outputting to strings.

    Returns
    -------
    joined_column : np.array (dtype=String)
        Value column joined with error column by a $\pm$ in each line.

    """

    if len(value_column) != len(error_column):
        raise ValueError('Columns must be the same length!')
    
    # We're going to implement this as a slow, loop-based thing first,
    # and then optimize it later array-like if necessary and if possible.

    joined_list = []

    for value, error in zip(value_column, error_column):

        rounded_value = np.round(value, precision)
        rounded_error = np.round(error, precision)
        
        joined_value_error = str(rounded_value)+r"$\pm$"+str(rounded_error)

        joined_list.append(joined_value_error)

    joined_column = np.array(joined_list)
    
    return joined_column

def convert_decimal_degree_columns_to_sexagesimal(ra_column, dec_column):
    """
    Turns a pair of decimal RA, Dec columns into sexagesimal columns.

    Like join_columns_with_plusminus(), this outputs an array of strings
    rather than an array of values, so this is really only useful if 
    you're going to write this as a LaTeX table.

    Output format: hh:mm:ss.s, +dd:mm:ss.ss

    Includes a sign on declination explicitly.
    Uses astrolib.coords.Position internally.

    Parameters
    ----------
    ra_column, dec_column : np.arrays
        Right Ascension and Declination, in decimal degrees.

    Returns
    -------
    ra_sex_column, dec_sex_column : np.arrays
        Right Ascension and Declination, in sexagesimal (hours, degrees)
        respectively. These are arrays of strings.

    """

    if len(ra_column) != len(dec_column):
        raise ValueError('Columns must be the same length!')

    sexagesimal_ra_list = []
    sexagesimal_dec_list = []

    for ra, dec in zip(ra_column, dec_column):

        sexagesimal_radec_string = coords.Position((ra, dec)).hmsdms()
        ra_sex_string, dec_sex_string = sexagesimal_radec_string.split()

        sexagesimal_ra_list.append(ra_sex_string)
        sexagesimal_dec_list.append(dec_sex_string)

    ra_sex_column = np.array(sexagesimal_ra_list)
    dec_sex_column = np.array(sexagesimal_dec_list)

    return ra_sex_column, dec_sex_column
    

def table_latex_strings_test():
    """ 
    This is a 'test' for generating pretty LaTeX-style tables.

    In particular, I want to see if I can make a) sexagesimal coordinate output
    and b) value \pm errorbar columns.

    See 
    https://github.com/YSOVAR/YSOVAR/blob/master/docs/workflow.rst 
    and
    http://docs.astropy.org/en/v0.2.1/_generated/astropy.io.ascii.latex.Latex.html
    for reference.
    
    """

    table = astropy.table.Table()
    table.table_name = "Table 1"

    # Be careful about this. Make sure you don't get the order of the args confused.
    addc = lambda name, data: table.add_column( 
        astropy.table.Column(name=name, data=data) )

    sexagesimal_RA, sexagesimal_Dec = convert_decimal_degree_columns_to_sexagesimal(
        np.degrees(ukvar_spread.RA), np.degrees(ukvar_spread.DEC))

    j_value_pm_error = join_columns_with_plusminus( ukvar_spread.j_median, 
                                                    ukvar_spread.j_err_median)
    
    addc('UKvar ID', ukvar_spread.UKvar_ID)
    addc('R.A.', sexagesimal_RA)
    addc('Decl.', sexagesimal_Dec)
    addc('Median J mag', j_value_pm_error)

    return table

    
