"""
A script that mates tables in the Orion catalog.

I hope to be able to implement this in two pieces:
1. A generic table-mating module that could be adapted to anything,
2. A script that uses (1) and the filepaths of the actual tables that I
   downloaded to actually perform the mergers.

The two-pieced-ness could be either two files or a single one 
(with some "only execute this part if this is __main__" magic, or something).

Heavy (or at least central) dependency on the functions I wrote a long time
ago in `match.py` is expected.

"""

import numpy as np

import atpy

import official_star_counter as osc

# I think I'm gonna have to make a Table_Parameters class
class TableParameters(object):
    """
    Contains the parameters we need in order to do the matching!
    
    """
    
    def __init__(self, path, alias, full_name, 
                 ra_cols, dec_cols, radec_fmt,
                 name_col, max_match = 1.0, data=None):
        """
        Initializing method.

        Parameters
        ----------
        path : str or None
            The location of the file containing our table data.
            Only use None if `data` is specified.
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
        if data = None:
            try:
                self.data = atpy.Table(path)
            except IOError:
                raise IOError("File '%s' not found" % path)
            except Exception, e:
                raise e
        elif type(data) is atpy.basetable.Table:
            self.data = data
            self.path = None
        else:
            raise Exception("Data in `data` is invalid.")

        # Is this sloppy? See http://stackoverflow.com/questions/12191075/is-there-a-shortcut-for-self-somevariable-somevariable-in-a-python-class-con
        self.path = path
        self.alias = alias
        self.full_name = full_name
        self.ra_cols, self.dec_cols = ra_cols, dec_cols
        self.radec_fmt = radec_fmt
        self.name_col = name_col
        self.max_match = max_match



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
        
    """

    # First, 

    for st in secondary_table_list:
        
        # Determine or construct decimal-degree RA and Dec columns.
        if 'sex' in st.radec_fmt.lower():
            # For each row 
            pass # until I implement the above
        elif len(ra_cols) == len(dec_cols) == 1:
            if 'deg' in 
                



def test():
    """
    Uses the above code to generate a simple test match-table.

    """
       
    # WFCAM Orion Variables - autovars, strict
    wov_avs_data = atpy.Table(osc.autovars_strict)

    chs = TableParameters(
        # path
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

    
    
        
        
        



    
