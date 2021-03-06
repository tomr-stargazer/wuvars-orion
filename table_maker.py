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
import sys
import fileinput

try:
    import coords
except ImportError:
    import astrolib.coords as coords

import astropy.io.ascii as ascii
import astropy.table

# All of these imports are meant to mirror those from figure_maker.
from official_star_counter import *
from color_slope_filtering import (jhk_empty, jhk_filled, jh_empty, jh_filled,
                                   hk_empty, hk_filled, filter_color_slopes)
from tablemate_comparisons import (mated_ukvar, ukvar_spread, 
                                   ukvar_periods, source_period_digger)
from tablemate_script import (Megeath2012, Megeath_P, Megeath_D,
                              Megeath_Full, Megeath_Allgoodsources,
                              XMM_north, Rice_UKvars)
from tablemate_core import index_secondary_by_primary, tablemater

# from montage_script import conf_subj_periodics, conf_subj_nonpers

dropbox_bo = os.path.expanduser("~/Dropbox/Bo_Tom/")
output_directory = dropbox_bo+"paper/publication_tables/"


# Let's grab IRAC colors from Megeath.
megeath2012_by_ukvar = index_secondary_by_primary(mated_ukvar, 
                                                  Megeath2012)
megeath2012_full_by_ukvar = index_secondary_by_primary(mated_ukvar, 
                                                       Megeath_Full)
megeath2012_all_by_ukvar = index_secondary_by_primary(mated_ukvar,
                                                      Megeath_Allgoodsources)

# XMM catalog gets matched too.
XMM_north_by_ukvar = index_secondary_by_primary(
    tablemater(Rice_UKvars, [XMM_north]), XMM_north)

# And let's make some color slope references that we like.
jhk_slope_reference = filter_color_slopes(autovars_strict, 'jhk',
                                          slope_confidence=0.5)
jh_slope_reference = filter_color_slopes(autovars_true, 'jh',
                                         slope_confidence=0.5)
hk_slope_reference = filter_color_slopes(autovars_true, 'hk',
                                         slope_confidence=0.5)

def clobber_table_write(table, filename, **kwargs):
    """ Writes a table, even if it has to clobber an older one. """

    try:
        table.write(filename, **kwargs)
    except Exception, e: 
        print e
        print "Overwriting file."
        os.remove(filename)
        table.write(filename, **kwargs)

def convert_tabletabular_to_deluxetable(file_path):
    """
    Directly modifies a .tex table file and makes it a compliant deluxetable.

    Expected input begins with
        \begin{table}
        \begin{tabular}{cc...cc}

    and ends with
        \end{tabular}
        \end{table} .

    The lines with {table} get deleted wholesale, and all appearances of
    'tabular' get replaced with 'deluxetable'.

    Don't put anything before the \begin{tabular} or after the \end{tabular}.

    Parameters
    ----------
    file_path : string
        Location of the .tex file containing the deluxetable-less table.

    """

    for line in fileinput.input(file_path, inplace=True):
        # Delete the \begin{table} and \end{table} lines.
        if "{table}" in line:
            sys.stdout.write("")
        # Convert tabular into deluxetable.
        elif 'tabular' in line:
            line = line.replace('tabular', 'deluxetable')
            sys.stdout.write(line)
        # Leave all the remaining lines alone.
        else:
            sys.stdout.write(line)

def make_megeath_class_column():
    """
    Generates a Class column from the Megeath data.

    For Disks and Protostars, the Class comes straight from
    megeath2012_by_ukvar. But there are two other classes:
    'ND' (no disk) which are sources in Megeath_allgoodsources_by_ukvar
    that are NOT in megeath2012_by_ukvar; and 'na' (blank),
    which are the 'orphans' and Megeath-matches-with-poor-Spitzer-photometry.

    """

    megeath_class_column = np.copy(megeath2012_by_ukvar.Class)

    for i in range(len(megeath_class_column)):
        if (megeath_class_column[i] == 'na' and
            megeath2012_all_by_ukvar.IDL_index[i] > 0) :
            megeath_class_column[i] = 'ND'

    return megeath_class_column


def make_xmm_class_column():
    """
    Generates a Class column from the XMM data.

    Prostar: data.proto == 1
    Disk: data.disks == 1
    C3: data.c3cnd == '1'
    na: all three of those zero.
    
    """

    xmm_class_column = np.zeros_like(XMM_north_by_ukvar.disks, dtype='|S2')

    for i in range(len(xmm_class_column)):
        
        if XMM_north_by_ukvar.proto[i] == 1: xmm_class_column[i] = 'P'

        elif XMM_north_by_ukvar.disks[i] == 1: xmm_class_column[i] = 'D'

        elif XMM_north_by_ukvar.c3cnd[i] == '1': xmm_class_column[i] = 'C3'

        elif ((XMM_north_by_ukvar.proto[i] == 0) & 
              (XMM_north_by_ukvar.disks[i] == 0) & 
              (XMM_north_by_ukvar.c3cnd[i] == '0')): xmm_class_column[i] = 'na'
        else:
            xmm_class_column[i] = 'na'
        
    return xmm_class_column

        
def t_table1_radec_xref_jhk_irac(write=False):
    """
    Generates Table 1.

    Current columns:
      ONCvar ID : int  ## note: this comes from our internal UKvar_ID column.
      RA : float, degrees
      DEC : float, degrees
      X-ref : string # Using SIMBAD names for now.
      Data quality : int (0, 1, 2) corresponding to subjective/auto/strict
      Periodic : int (0, 1)
      Median J, H, K, with error bars : six floats
      IRAC colors from Megeath, and errors : eight floats
      Class from Megeath : string {'P', 'D', 'ND', or 'na'}

    Parameters
    ----------
    write : bool, optional (default False)
        Write to disk? Either way, this function returns an ATpy table.
      
    Returns
    -------
    table : atpy.Table
        Table 1.

    """

    table = astropy.table.Table()
    table.table_name = "Table 1"

    columns_data_and_formats = [
        ('ONCvar ID', ukvar_spread.UKvar_ID, '%i'),
        ('R.A. (deg)', np.degrees(ukvar_spread.RA), '%.6f'),
        ('Decl. (deg)', np.degrees(ukvar_spread.DEC), '%.6f'),
        ('SIMBAD Cross-reference', ukvar_spread.SIMBAD_name, '%s'),
        ('Data quality flag', ukvar_spread.autovar + ukvar_spread.strict, '%i'),
        ('Periodic flag', ukvar_spread.periodic, '%i'),
        ('Median J mag', ukvar_spread.j_median, '%.3f'),
        ('Median J mag error', ukvar_spread.j_err_median, '%.3f'),
        ('Median H mag', ukvar_spread.h_median, '%.3f'),
        ('Median H mag error', ukvar_spread.h_err_median, '%.3f'),
        ('Median K mag', ukvar_spread.k_median, '%.3f'),
        ('Median K mag error', ukvar_spread.k_err_median, '%.3f'),
        ('Spitzer [3.6] mag', megeath2012_full_by_ukvar['3.6'], '%.3f'),
        ('Spitzer [3.6] mag error', megeath2012_full_by_ukvar['e_3.6'], '%.3f'),
        ('Spitzer [4.5] mag', megeath2012_full_by_ukvar['4.5'], '%.3f'),
        ('Spitzer [4.5] mag error', megeath2012_full_by_ukvar['e_4.5'], '%.3f'),
        ('Spitzer [5.8] mag', megeath2012_full_by_ukvar['5.8'], '%.3f'),
        ('Spitzer [5.8] mag error', megeath2012_full_by_ukvar['e_5.8'], '%.3f'),
        ('Spitzer [8.0] mag', megeath2012_full_by_ukvar['8'], '%.3f'),
        ('Spitzer [8.0] mag error', megeath2012_full_by_ukvar['e_8'], '%.3f'),
        ('Class (from Megeath et al. 2012)', make_megeath_class_column(), '%s') ]

    column_to_format = {}
    for column, data, format in columns_data_and_formats:
        table[column] = data
        column_to_format[column] = format

    if write:
        table.write(output_directory+'AJ_table_2.txt', format='ascii.basic', delimiter="&", formats=column_to_format)


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

def t_table2_variability_periods_periodics_bymegeathclass(write=False):
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


    Parameters
    ----------
    write : bool, optional (default False)
        Write to disk? Either way, this function returns an ATpy table.
      
    """

    table = astropy.table.Table()
    table.table_name = "Table 2"

    periodics = ukvar_spread.where(ukvar_spread.periodic != 0)
    periodic_periods = ukvar_periods[ukvar_spread.periodic != 0]
    megeath_class_by_periodics = make_megeath_class_column()[ukvar_spread.periodic != 0]

    # Do some stuff where we blank out color slopes that are no good
    jhk_slope_column = periodics.jhk_slope
    jhk_slope_error = periodics.jhk_slope_err
    jhk_slope_column[~np.in1d(periodics.SOURCEID,
                              jhk_slope_reference.SOURCEID)] = np.nan
    jhk_slope_error[~np.in1d(periodics.SOURCEID,
                             jhk_slope_reference.SOURCEID)] = np.nan

    jjh_slope_column = periodics.jjh_slope
    jjh_slope_error = periodics.jjh_slope_err
    jjh_slope_column[~np.in1d(periodics.SOURCEID,
                              jh_slope_reference.SOURCEID)] = np.nan
    jjh_slope_error[~np.in1d(periodics.SOURCEID,
                             jh_slope_reference.SOURCEID)] = np.nan

    khk_slope_column = periodics.khk_slope
    khk_slope_error = periodics.khk_slope_err
    khk_slope_column[~np.in1d(periodics.SOURCEID,
                              hk_slope_reference.SOURCEID)] = np.nan
    khk_slope_error[~np.in1d(periodics.SOURCEID,
                             hk_slope_reference.SOURCEID)] = np.nan

    columns_data_and_formats = [
        ('ONCvar ID', periodics.UKvar_ID, '%i'),
        ('N_J', periodics.N_j, '%i'),
        ('N_H', periodics.N_h, '%i'),
        ('N_K', periodics.N_k, '%i'),
        ('J mag range (robust)', periodics.j_ranger, '%.3f'),
        ('H mag range (robust)', periodics.h_ranger, '%.3f'),
        ('K mag range (robust)', periodics.k_ranger, '%.3f'),
        ('J-H range (robust)', periodics.jmh_ranger, '%.3f'),
        ('H-K range (robust)', periodics.hmk_ranger, '%.3f'),
        ('(J-H), (H-K) color slope', jhk_slope_column, '%.3f'),
        ('jhk_slope_error', jhk_slope_error, '%.3f'),
        ('J, (J-H) color slope', jjh_slope_column, '%.3f'),
        ('jjh_slope_error', jjh_slope_error, '%.3f'),
        ('K, (H-K) color slope', khk_slope_column, '%.3f'),
        ('khk_slope_error', khk_slope_error, '%.3f'),
        ('Stetson Variability Index', periodics.Stetson, '%.3f'),
        ('Bands used to compute Stetson', periodics.Stetson_choice, '%s'),
        ('Best-fit period', periodic_periods, '%.4f'),
        ('Data quality flag', periodics.autovar + periodics.strict, '%i'),
        ('Class', megeath_class_by_periodics, '%s')
    ]

    column_to_format = {}
    for column, data, format in columns_data_and_formats:
        table[column] = data
        column_to_format[column] = format


    if write:
        table.write(output_directory+"AJ_table_4.txt", format='ascii.basic', delimiter="&", formats=column_to_format)

    return table

def t_table3_variability_nonperiodics_bymegeathclass(write=False):
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

    Parameters
    ----------
    write : bool, optional (default False)
        Write to disk? Either way, this function returns an ATpy table.

    """

    table = astropy.table.Table()
    table.table_name = "Table 3"

    nonperiodics = ukvar_spread.where(ukvar_spread.periodic == 0)
    megeath_class_by_nonperiodics = make_megeath_class_column()[ukvar_spread.periodic == 0]

    # Do some stuff where we blank out color slopes that are no good
    jhk_slope_column = nonperiodics.jhk_slope
    jhk_slope_error = nonperiodics.jhk_slope_err
    jhk_slope_column[~np.in1d(nonperiodics.SOURCEID, jhk_slope_reference.SOURCEID)] = np.nan
    jhk_slope_error[~np.in1d(nonperiodics.SOURCEID, jhk_slope_reference.SOURCEID)] = np.nan

    jjh_slope_column = nonperiodics.jjh_slope
    jjh_slope_error = nonperiodics.jjh_slope_err
    jjh_slope_column[~np.in1d(nonperiodics.SOURCEID, jh_slope_reference.SOURCEID)] = np.nan
    jjh_slope_error[~np.in1d(nonperiodics.SOURCEID, jh_slope_reference.SOURCEID)] = np.nan

    khk_slope_column = nonperiodics.khk_slope
    khk_slope_error = nonperiodics.khk_slope_err
    khk_slope_column[~np.in1d(nonperiodics.SOURCEID, hk_slope_reference.SOURCEID)] = np.nan
    khk_slope_error[~np.in1d(nonperiodics.SOURCEID, hk_slope_reference.SOURCEID)] = np.nan

    columns_data_and_formats = [
        ('ONCvar ID', nonperiodics.UKvar_ID, '%i'),
        ('N_J', nonperiodics.N_j, '%i'),
        ('N_H', nonperiodics.N_h, '%i'),
        ('N_K', nonperiodics.N_k, '%i'),
        ('J mag range (robust)', nonperiodics.j_ranger, '%.3f'),
        ('H mag range (robust)', nonperiodics.h_ranger, '%.3f'),
        ('K mag range (robust)', nonperiodics.k_ranger, '%.3f'),
        ('J-H range (robust)', nonperiodics.jmh_ranger, '%.3f'),
        ('H-K range (robust)', nonperiodics.hmk_ranger, '%.3f'),
        ('(J-H), (H-K) color slope', jhk_slope_column, '%.3f'),
        ('jhk_slope_error', jhk_slope_error, '%.3f'),
        ('J, (J-H) color slope', jjh_slope_column, '%.3f'),
        ('jjh_slope_error', jjh_slope_error, '%.3f'),
        ('K, (H-K) color slope', khk_slope_column, '%.3f'),
        ('khk_slope_error', khk_slope_error, '%.3f'),
        ('Stetson Variability Index', nonperiodics.Stetson, '%.3f'),
        ('Bands used to compute Stetson', nonperiodics.Stetson_choice, '%s'),
        ('Data quality flag', nonperiodics.autovar + nonperiodics.strict, '%i'),
        ('Class', megeath_class_by_nonperiodics, '%s')
        ]

    # Now split it into three pieces and compute medians!
    column_to_format = {}
    for column, data, format in columns_data_and_formats:
        table[column] = data
        column_to_format[column] = format

    if write:
        table.write(output_directory+"AJ_table_5.txt", format='ascii.basic', delimiter="&", formats=column_to_format)

    return table
    
         
def t_table0_crossref(write=False):
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

    if write:
        clobber_table_write(table, output_directory+"Table_0.txt", type='ascii')
        clobber_table_write(table, output_directory+"Table_0.fits")

    return table

def join_columns_with_plusminus(value_column, error_column=None, precision=3,
                                null_input=np.double(-9.99999488e+08),
                                null_output=' ', lstrip_zero_error=True,
                                omit_pm_and_error=False):
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
    null_input : float, optional
        An input value that you want masked to `null_output` before joining 
        things together.
    null_output : string, optional
        The output string you want to use in place of null_input.
    lstrip_zero_error : bool, optional
        Remove a leading zero from the error term? Defaults True.
    omit_pm_and_error : bool, optional
        Discard the \pm and error term completely? Defaults False.
        Useful if you just wanted to round and filter out bad values.

    Returns
    -------
    joined_column : np.array (dtype=String)
        Value column joined with error column by a $\pm$ in each line.

    """

    if error_column == None:
        omit_pm_and_error = True
        error_column = np.zeros_like(value_column)
    elif len(value_column) != len(error_column):
        raise ValueError('Columns must be the same length!')
    
    # We're going to implement this as a slow, loop-based thing first,
    # and then optimize it later array-like if necessary and if possible.

    joined_list = []

    for value, error in zip(value_column, error_column):

        # Some complicated handling of null_inputs and null_outputs.
        if error == null_input and value != null_input:
            raise ValueError("An error is null_input but its value is not!")
        if value == null_input or np.isnan(value):

            joined_list.append(null_output)
            continue

        rounded_value = "%.*f" % (precision, value)
        rounded_error = "%.*f" % (precision, error)

        if lstrip_zero_error:
            rounded_error = rounded_error.lstrip('0')
        
        joined_value_error = rounded_value+r"$\pm$"+rounded_error

        if omit_pm_and_error:
            # This is not the usual use case.
            joined_list.append(rounded_value) 
        else:
            joined_list.append(joined_value_error)

    joined_column = np.array(joined_list)
    
    return joined_column

def make_column_pretty(value_column, **kwargs):
    
    return join_columns_with_plusminus(value_column, 
                                       error_column=None, **kwargs)

def convert_decimal_degree_columns_to_sexagesimal(ra_column, dec_column,
                                                  ra_truncate=0,
                                                  dec_truncate=0):
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
    ra_truncate, dec_truncate : int, optional
        How many decimal places to delete from the end of each coordinate,
        respectively.

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

        if ra_truncate > 0:
            ra_sex_string = ra_sex_string[:-ra_truncate]
        if dec_truncate > 0:
            dec_sex_string = dec_sex_string[:-dec_truncate]

        sexagesimal_ra_list.append(ra_sex_string)
        sexagesimal_dec_list.append(dec_sex_string)

    ra_sex_column = np.array(sexagesimal_ra_list)
    dec_sex_column = np.array(sexagesimal_dec_list)

    return ra_sex_column, dec_sex_column

def write_and_correct_latex_table(table, filename, caption, begin=0, end=30,
                                  **kwargs):
    # 1. Convert all the column headers to colhead { old_name }
    for colname in table.colnames:
        table[colname].name = "\\colhead{ %s }" % colname

    # 2. Prepare the latexdict
    header_start = ('\\tabletypesize{\\scriptsize}' +
                    '\n\\rotate\n' +
                    ('\\tablecaption{ %s }\n' % caption) +
                    '\\tablewidth{0pt}\n\n')
    data_start = r'\startdata'
    data_end = r'\enddata'

    latexdict = {
        'header_start': header_start+r'\tablehead{',
        'header_end': '}',
        'data_start': data_start,
        'data_end': data_end
        }

    latexdict.update(kwargs)
    
    # 3. Write the table as a {table} and {tabular} thing
    ascii.write(
        table[begin:end], filename,
        Writer = ascii.Latex,
        latexdict = latexdict,
        )

    # 4. Convert it from {table}+{tabular} environment to {deluxetable}
    convert_tabletabular_to_deluxetable(filename)


def table_latex_strings_test(write=False, begin=0, end=30):
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

    sexagesimal_RA, sexagesimal_Dec = (
        convert_decimal_degree_columns_to_sexagesimal(
            np.degrees(ukvar_spread.RA), np.degrees(ukvar_spread.DEC)) )

    j_value_pm_error = join_columns_with_plusminus(ukvar_spread.j_median,
                                                   ukvar_spread.j_err_median,
                                                   precision=2)
    
    addc('ONCvar ID', ukvar_spread.UKvar_ID)
    addc('R.A.', sexagesimal_RA)
    addc('Decl.', sexagesimal_Dec)
    addc('Median J mag', j_value_pm_error)

    if write:
        filename = output_directory+"Table_test.tex" 
        write_and_correct_latex_table(table, filename, 
                                      "Basic Properties of Stars")
    return table

def table1_latex_output(write=False, begin=0, end=30,
                        omit_spitzer_errors=False):
    """
    Morphs Table 1 into a LaTeX-friendly output and writes it to a .tex file.

    """

    # Load up the table you want to transform to LaTeX.
    table1_data = t_table1_radec_xref_jhk_irac()

    latex_table = astropy.table.Table()
    latex_table.table_name = "Table 1"

    # Make sure you don't get the order of the args confused.
    addc = lambda name, data: latex_table.add_column( 
        astropy.table.Column(name=name, data=data) )

    sexagesimal_RA, sexagesimal_Dec = (
        convert_decimal_degree_columns_to_sexagesimal(
            table1_data['R.A. (deg)'], table1_data['Decl. (deg)'],
            ra_truncate=1, dec_truncate=2) )

    # Let's "compress" the SIMBAD column.
    simbad_compressed = []
    for simbad_id in table1_data['SIMBAD Cross-reference']:
        if "2MASS J" in simbad_id:
            simbad_id = simbad_id.replace("2MASS J", "2M")
        simbad_compressed.append(simbad_id)

    photometry_column_names = [
        'Median J mag',
        'Median H mag',
        'Median K mag',
        'Spitzer [3.6] mag',
        'Spitzer [4.5] mag',
        'Spitzer [5.8] mag',
        'Spitzer [8.0] mag']

    error_column_names = [x + " error" for x in photometry_column_names]

    new_column_names = [
        '$J$',
        '$H$',
        '$K$',
        '[3.6]',
        '[4.5]',
        '[5.8]',
        '[8.0]']

    # There must be a less bonehead way to do this...
    addc('ID', table1_data['ONCvar ID'])
    addc(r'$\textrm{RA}_{J2000}$', sexagesimal_RA)
    addc(r'$\textrm{Dec}_{J2000}$', sexagesimal_Dec)
    addc('SIMBAD alt. ID', simbad_compressed)
    addc('Q', table1_data['Data quality flag'].astype('int'))
    addc('P', table1_data['Periodic flag'].astype('int'))

    joined_column_list = []

    if omit_spitzer_errors:
        # This array says "drop the error terms on the Spitzer mags"
        # when we feed them into join_whatever.
        omit_errorbar_list = [False]*3 + [True]*4
    else:
        omit_errorbar_list = [False]*7

    # Let's create a bunch of mag \pm error columns.
    for photometry_column, error_column, omit_errorbar in zip(
            photometry_column_names, error_column_names, omit_errorbar_list):

        joined_column = join_columns_with_plusminus(
            table1_data[photometry_column], table1_data[error_column],
            precision=2, 
            null_input=np.nanmin(table1_data[photometry_column]),
            null_output=r'\ldots', omit_pm_and_error=omit_errorbar)
        
        joined_column_list.append(joined_column)


    for joined_column, column_name in zip(joined_column_list, 
                                          new_column_names):
        addc(column_name, joined_column)

    addc('Class', table1_data['Class (from Megeath et al. 2012)'])


    if write:
        filename = output_directory+"Table_1.tex" 

        col_align = "ccccccrrrrrrrc"
        
        write_and_correct_latex_table(latex_table, filename, 
                                      "Basic Properties of Stars",
                                      begin=begin, end=end,
                                      col_align = col_align)

    return latex_table

def table2_latex_output(write=False, begin=0, end=30, decimal_precision=2):
    """
    Morphs Table 2 into a LaTeX-friendly output and writes it to a .tex file.

    """

    table2_data = t_table2_variability_periods_periodics_bymegeathclass()

    latex_table = astropy.table.Table()
    latex_table.table_name = "Table 2"

    addc = lambda name, data: latex_table.add_column( 
        astropy.table.Column(name=name, data=data) )

    # reorder the table by Class
    class_number = np.zeros(table2_data.Class.size)+4.
    class_number[table2_data.Class == 'P'] = 1
    class_number[table2_data.Class == 'D'] = 2
    class_number[table2_data.Class == 'ND'] = 3
    table2_data.add_column("class_number", class_number)

    table2_data.sort('class_number')

    addc('ID', table2_data['ONCvar ID'])
    addc('$N_J$', table2_data.N_J)
    addc('$N_H$', table2_data.N_H)
    addc('$N_K$', table2_data.N_K)
    addc(r'$\Delta K$', 
         make_column_pretty(table2_data['K mag range (robust)'], precision=2,
                            null_output='\ldots'))
    addc(r'$\Delta J-H$', 
         make_column_pretty(table2_data['J-H range (robust)'], precision=2,
                            null_output='\ldots'))
    addc(r'$\Delta H-K$', 
         make_column_pretty(table2_data['H-K range (robust)'], precision=2,
                            null_output='\ldots'))
    addc("$m(J-H,H-K)$",
         join_columns_with_plusminus(
             table2_data['(J-H), (H-K) color slope'], 
             table2_data.jhk_slope_error, precision=2, 
             null_output='\ldots'))
    addc("$m(J,J-H)$",
         join_columns_with_plusminus(
             table2_data['J, (J-H) color slope'], 
             table2_data.jjh_slope_error, precision=2, 
             null_output='\ldots'))
    addc("$m(K,H-K)$",
         join_columns_with_plusminus(
             table2_data['K, (H-K) color slope'], 
             table2_data.khk_slope_error, precision=2, 
             null_output='\ldots'))
    addc("$S$", make_column_pretty(
        table2_data['Stetson Variability Index'], precision=2))
    addc("Period", make_column_pretty(table2_data['Best-fit period'],
                                      precision=4))

    if write:
        filename = output_directory+"Table_2.tex"

        namestring = r"""Variability properties of periodic stars
		\label{tab:var_periodics}"""

        write_and_correct_latex_table(
            latex_table, filename, namestring,
            begin=begin, end=end)
        
    return latex_table

def table3_latex_output(write=False, begin=0, end=30, decimal_precision=2):
    """
    Morphs table 3 into a LaTeX-friendly output and writes it to a .tex file.

    """

    table3_data = t_table3_variability_nonperiodics_bymegeathclass()

    latex_table = astropy.table.Table()
    latex_table.table_name = "table 3"

    addc = lambda name, data: latex_table.add_column( 
        astropy.table.Column(name=name, data=data) )

    # reorder the table by Class
    class_number = np.zeros(table3_data.Class.size)+4.
    class_number[table3_data.Class == 'P'] = 1
    class_number[table3_data.Class == 'D'] = 2
    class_number[table3_data.Class == 'ND'] = 3
    table3_data.add_column("class_number", class_number)

    table3_data.sort('class_number')

    addc('ID', table3_data['ONCvar ID'])
    addc('$N_J$', table3_data.N_J)
    addc('$N_H$', table3_data.N_H)
    addc('$N_K$', table3_data.N_K)
    addc(r'$\Delta K$', 
         make_column_pretty(table3_data['K mag range (robust)'], precision=2,
                            null_output='\ldots'))
    addc(r'$\Delta J-H$', 
         make_column_pretty(table3_data['J-H range (robust)'], precision=2,
                            null_output='\ldots'))
    addc(r'$\Delta H-K$', 
         make_column_pretty(table3_data['H-K range (robust)'], precision=2,
                            null_output='\ldots'))
    addc("$m(J-H,H-K)$",
         join_columns_with_plusminus(
             table3_data['(J-H), (H-K) color slope'], 
             table3_data.jhk_slope_error, precision=2, 
             null_output='\ldots'))
    addc("$m(J,J-H)$",
         join_columns_with_plusminus(
             table3_data['J, (J-H) color slope'], 
             table3_data.jjh_slope_error, precision=2, 
             null_output='\ldots'))
    addc("$m(K,H-K)$",
         join_columns_with_plusminus(
             table3_data['K, (H-K) color slope'], 
             table3_data.khk_slope_error, precision=2, 
             null_output='\ldots'))
    addc("$S$", make_column_pretty(
        table3_data['Stetson Variability Index'], precision=2))

    if write:
        filename = output_directory+"Table_3.tex"

        namestring = r"""Variability properties of nonperiodic stars
		\label{tab:var_nonperiodics}"""

        write_and_correct_latex_table(
            latex_table, filename, namestring,
            begin=begin, end=end)
        
    return latex_table
