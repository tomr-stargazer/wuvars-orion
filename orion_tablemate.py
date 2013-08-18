"""
A module for mating tables in the Orion catalog.

I hope to be able to implement this in two pieces:
1. A generic table-mating module that could be adapted to anything,
2. A script that uses (1) and the filepaths of the actual tables that I
   downloaded to actually perform the mergers.

The two-pieced-ness could be either two files or a single one 
(with some "only execute this part if this is __main__" magic, or something).

Heavy (or at least central) dependency on the functions I wrote a long time
ago in `match.py` is expected.

"""

import copy

import numpy as np

import atpy
import coords

import match
import official_star_counter as osc

# I think I'm gonna have to make a Table_Parameters class
class TableParameters(object):
    """
    Contains the parameters we need in order to do the matching!
    
    """
    
    def __init__(self, data, alias, full_name, 
                 ra_cols, dec_cols, radec_fmt,
                 name_col, max_match = 1.0):
        """
        Initializing method.

        Parameters
        ----------
        data : str or atpy.Table
            The location of the file containing our table data, OR
            an atpy.Table object containing the data itself.
        alias : str
            A consise string describing the table's name.
        full_name : str
            The full name of the table, including the name 
            and reference of the article it came from.
        ra_cols, dec_cols : list of str
            Which column(s) contain RA and DEC data, respectively.
        radec_fmt : str
            Information on how the RA and DEC columns store their data.
        name_col : int or str
            An index or name of the column containing names in this table.
        max_match : float, optional
            Largest possible match radius for this table, in arcseconds. 
            Default value: 1.0
        data : atpy.Table
        
        """

        # We're gonna check to make sure that the provided filepath is valid.
        # If it's not, throw some exceptions around.
        if type(data) is atpy.basetable.Table:
            self.data = data
            self.path = None
        elif type(data) is str:
            try:
                self.path = data
                self.data = atpy.Table(self.path)
            except IOError:
                raise IOError("File '%s' not found" % data)
            except Exception, e:
                raise e
        else:
            raise Exception("Data in `data` is invalid.")

        # Is this sloppy? See http://stackoverflow.com/questions/12191075/is-there-a-shortcut-for-self-somevariable-somevariable-in-a-python-class-con
        self.alias = alias
        self.full_name = full_name
        self.ra_cols, self.dec_cols = ra_cols, dec_cols
        self.radec_fmt = radec_fmt
        self.name_col = name_col
        self.max_match = max_match

        # Now, the logic that makes the RA and Dec columns uniform.
        
        # Now, we'll need to extract the RA and Dec information.
        # This is actually something that needs to be done uniformly to every
        # single table object, so I think I should actually stick it in the
        # class constructor so it's done at initialization and never worried
        # about ever again!
        # Namely, semantics to take the RA/Dec columns and the provided radec_fmt
        # and append an .RA and a .DEC to the TableParameters object itself
        # that's in a standard decimal-degrees format.
        # So that we never have to worry about that in the tablemater() function
        # itself.
        # okay, that's the goal for next session: put the format-parsing code
        # in the __init__ method!

        # What cases are there? 
        # 1. Simple: single-column, decimal format (degrees, hours, or radians)
        # 2. Complex SC: single-column of STRINGS in sex format 
        # 3. Complex TC: triple-column of numbers or strings in sex format
        # 4. "other"

        # Determine or construct decimal-degree RA and Dec columns.

        # Simple case: single-column, decimal format
        if (not 'sex' in radec_fmt.lower()) and (len(ra_cols) == len(dec_cols) == 1):
            print "Case 1"
            ra_raw = self.data[ra_cols[0]]
            dec_raw = self.data[dec_cols[0]]

            # Is RA in hours? (unlikely!)
            if 'hours' in radec_fmt.lower():
                # put the RA from hours to degrees 
                self.RA = ra_raw * 15
                self.DEC = dec_raw
            # Are we in degrees?
            elif 'deg' in radec_fmt.lower():
                self.RA = ra_raw
                self.DEC = dec_raw
            # Are we in radians?
            elif 'rad' in radec_fmt.lower():
                self.RA = np.degrees(ra_raw)
                self.DEC = np.degrees(dec_raw)

        # More complicated: triple-column, sexagesimal format.
        elif 'sex' in radec_fmt.lower():
            if len(ra_cols) == len(dec_cols) == 3:

                print "Case 3"

                rhcol, rmcol, rscol = (self.data[ra_cols[0]],
                                       self.data[ra_cols[1]],
                                       self.data[ra_cols[2]])
                ddcol, dmcol, dscol = (self.data[dec_cols[0]],
                                       self.data[dec_cols[1]],
                                       self.data[dec_cols[2]])
                
                ra_decimal = []
                dec_decimal = []
                
                for (rh, rm, rs, 
                     dd, dm, ds) in zip( rhcol, rmcol, rscol,
                                         ddcol, dmcol, dscol ):
                     coord_string = ("%02d:%02d:%05.2f %03d:%02d:%05.2f" %
                                     (rh, rm, rs, dd, dm, ds) )
                     coord = coords.Position( coord_string )
                     radec_dd = coord.dd()
                     
                     ra_decimal.append( radec_dd[0] )
                     dec_decimal.append( radec_dd[1] )
                
                self.RA = np.array(ra_decimal)
                self.DEC = np.array(dec_decimal)

# This is if the SIGN (+/-) of the Declination is stored as its own column.
            elif len(dec_cols) == 4:

                print "Case 3.5"

                rhcol, rmcol, rscol = (self.data[ra_cols[0]],
                                       self.data[ra_cols[1]],
                                       self.data[ra_cols[2]])
                sign_col, ddcol, dmcol, dscol = (self.data[dec_cols[0]],
                                                 self.data[dec_cols[1]],
                                                 self.data[dec_cols[2]],
                                                 self.data[dec_cols[3]])
                
                ra_decimal = []
                dec_decimal = []
                
                for (rh, rm, rs, sign,
                     dd, dm, ds) in zip( rhcol, rmcol, rscol, sign_col,
                                         ddcol, dmcol, dscol ):
                     coord_string = ("%02d:%02d:%05.2f %s%02d:%02d:%05.2f" %
                                     (rh, rm, rs, sign, dd, dm, ds) )
                     coord = coords.Position( coord_string )
                     radec_dd = coord.dd()
                     
                     ra_decimal.append( radec_dd[0] )
                     dec_decimal.append( radec_dd[1] )
                
                self.RA = np.array(ra_decimal)
                self.DEC = np.array(dec_decimal)

            else:
                print "I don't yet know how to deal with this."
                    
                
            # For each row 
            pass # until I implement the above
#        elif None
#            if 'deg' in 




def tablemater(primary_table, secondary_table_list):
    """ 
    Creates the mated table.

    Parameters
    ----------
    primary_table : TableParameters instance
        The primary catalog of stars we're matching to,
        as well any important associated information.
    secondary_table_list : array of TableParameters instance
        A list containing the other tables we're matching
        to our primary table, with their parameters.
    
    Returns
    -------
    mated_table : atpy.Table
        A catalog where each row corresponds to a star in `primary_table`
        and contains a cross-identification for the secondary_tables 
        in each column (or a sentinel value indicating failure to match).

        Indices start at zero.

        The mated table does not contain ANY extra information about any
        sources - not even RA/Dec, brightnesses, etc.
        (MAYBE a column or two saying if stars were automatic/subjective,
         and periodic/nonperiodic.)
        
    """

    # First, construct a table with columns belonging to Primary Table
    # : we'll be adding more columns later!

    mated_table = atpy.Table()

    mated_table.add_column( primary_table.alias+"_ID", 
                            primary_table.data[primary_table.name_col] )
    mated_table.add_column( primary_table.alias+"_index", 
                            np.arange(len(primary_table.data)) )

    pt = primary_table

    if type(secondary_table_list) is not list:
        secondary_table_list = [secondary_table_list]

    for st in secondary_table_list:
        
        # We are appending two columns to mated_table:
        #  secondary_table.alias+"_ID", (THING 1)
        #  secondary_table.alias+"_index", (THING 2)
        # where things 1 and 2 are created using match.core_match

        matches = match.core_match( pt.RA, pt.DEC, st.RA, st.DEC, 
                                    max_match=st.max_match, verbose=False)
        
        # I like this solution!
        mated_indices = matches[0]
        
        mated_names = st.data[st.name_col][mated_indices]
        # Enforce that -1 means failed match:
        mated_names[mated_indices == -1] = -1

        mated_table.add_column(st.alias+"_ID", mated_names)
        mated_table.add_column(st.alias+"_index", mated_indices)

    return mated_table


def index_secondary_by_primary(mated_table, secondary_table):
    """
    Indexes a secondary table by primary table IDs.

    Returns it as a new table; rows of the primary table that 
    did not match to the secondary table are present, filled 
    with np.nan, so that the columns from the returned table
    could be (in principle) appended directly to the primary
    table or used in some derivative product, such as a 
    publication table.

    Parameters
    ----------
    mated_table : atpy.Table
        Output of tablemater(). The first two columns of
        this table will be used as the "primary" index/ID.
    secondary_table : TableParameters instance
        Must be one of the secondary tables used to create
        mated_table.

    Returns
    -------
    secondary_indexed_by_primary : atpy.Table
        
    """

    # make an empty table
    secondary_indexed_by_primary = atpy.Table()

    # seed it
    first_column_name = mated_table.columns.keys[0]
    second_column_name = mated_table.columns.keys[1]

    # primary ID
    secondary_indexed_by_primary.add_column(
        first_column_name,
        mated_table[first_column_name] )
    # index in primary table
    secondary_indexed_by_primary.add_column(
        second_column_name,
        mated_table[second_column_name] )

    # name of secondary table in mated table
    secondary_alias = secondary_table.alias
    
    # index in secondary table
    secondary_indices_of_primary_rows = mated_table.data[secondary_alias+"_index"]
    # note that there are gonna be a lot of -1s in there.

    # do I want to do this column-by-column, or row-by-row? 
    # I think I prefer column-by-column, where I loop through
    # column names in the secondary

    for column_name in secondary_table.data.columns.keys:

        target_column = secondary_table.data[column_name]
        # so, two-step process for each column.
        # first, do a naive indexing
        column_indexed_by_primary = target_column[secondary_indices_of_primary_rows]
        # second, set all the [-1]s to nan or -9999 
        if issubclass(target_column.dtype.type, np.integer):
            column_indexed_by_primary[secondary_indices_of_primary_rows == -1] = -9999
        else:
            column_indexed_by_primary[secondary_indices_of_primary_rows == -1] = np.nan
        # then add the column by name to our new table
        secondary_indexed_by_primary.add_column(column_name,
                                                column_indexed_by_primary)

    # let's see if this works!
    return secondary_indexed_by_primary
        

def test():
    """
    Uses the above code to generate a simple test match-table.

    """
       
    # WFCAM Orion Variables - autovars, strict
    wov_avs_data = osc.autovars_strict
    
    wov_avs = TableParameters(
        #data
        wov_avs_data,
        #alias
        "WFCAM Orion",
        #full name
        "Strict automatic variables found in the WFCAM Orion monitoring survey. From 'High Amplitude and Periodic Near-Infrared Variables in the Orion Nebula Cluster' by Rice, Thomas S.; Reipurth, Bo; et al.",
        #ra_cols, dec_cols
        ['RA'], ['DEC'],
        #radec_fmt
        'decimal radians',
        #name_col
        'SOURCEID')

    # Carpenter Hillenbrand Skrutskie 2001: the other big Orion nir var study.

    chs = TableParameters(
        # data
        "/home/tom/reu/ORION/DATA/carpenter_table4.fits", 
        # alias
        "CHS2001",
        # full_name
        "Table 4. 'Near-Infrared Variable Stars', from 'Near-Infrared Photometric Variability of Stars Toward the Orion A Molecular Cloud' by Carpenter, John M.; Hillenbrand, Lynne A.; Skrutskie, M. F. 2001AJ....121.3160C",
        # ra_cols, dec_cols
        ['RAJ2000'], ['DEJ2000'],
        #radec_fmt
        'decimal degrees',
        #name_col
        '__CHS2001_')

    # This is Bo's Ha survey
    eso_ha = TableParameters(
        # data
        "/home/tom/reu/ORION/DATA/ESOHa_m42_fc_P_fits.fits", 
        # alias
        "ESO_Ha_PAR",
        # full_name
        "'ESO H-alpha survey of ONC, 5 x 5 degrees' by Petterson, B.; Armond, T.; & Reipurth, B. 2013, in prep.",
        # ra_cols, dec_cols
        ['R.A.(2000)', 'col7', 'col8'], ['Dec(2000)', 'col10', 'col11'],
        #radec_fmt
        'sex-three',
        #name_col
        '2MASS identity')

    megeath = TableParameters(
        data= atpy.Table(
            "/home/tom/Dropbox/Bo_Tom/aux_catalogs/Megeath2012_table1.txt", 
            type='ascii'),
        alias="Megeath2012",
        full_name="I'll do this later.",
        ra_cols = ['RAh', 'RAm', 'RAs'],
        dec_cols = ['DE-', 'DEd', 'DEm', 'DEs'],
        radec_fmt='sex-three-four',
        name_col='Num')

    # now that they're defined, match em!

    # Test 0: can we at least match to ourself?
    wov_avs2 = copy.copy(wov_avs)
    wov_avs2.alias = "WOO_TEST"
    test_mate0 = tablemater(wov_avs, [wov_avs2])

#    return test_mate0
    # Test 1: simple
    test_mate1 = tablemater(wov_avs, [chs])

#    return test_mate1

    # Test 2: harder, cuz a) multiple tables now and b) three-column sex
    test_mate2 = tablemater(wov_avs, [chs, eso_ha])

    # Test 3: even harder, cuz c) three/four-col sex

#    return test_mate2

    test_mate3 = tablemater(wov_avs, [chs, eso_ha, megeath])

    return test_mate3
