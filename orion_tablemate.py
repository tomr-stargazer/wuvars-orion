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

# I think I'm gonna have to make a Table_Parameters class
class TableParameters(object):
    """
    Contains the parameters we need in order to do the matching!
    
    """
    
    def __init__(self,  path, alias, full_name, 
                 ra_cols, ra_fmt, dec_cols, dec_fmt,
                 name_col, max_match = 1.0):
        """
        Initializing method.

        Parameters
        ----------
        path : str
            The location of the file containing our table data.
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
        
        """

        # We're gonna check to make sure that the provided filepath is valid.
        # If it's not, throw some exceptions around.
        try:
            self.data = atpy.Table(path)
        except IOError:
            raise IOError("File '%s' not found" % path)
        except Exception, e:
            raise e

        # Is this sloppy? See http://stackoverflow.com/questions/12191075/is-there-a-shortcut-for-self-somevariable-somevariable-in-a-python-class-con
        self.path = path
        self.alias = alias
        self.full_name = full_name
        self.ra_cols, self.dec_cols = ra_cols, dec_cols
        self.radec_fmt = radec_fmt
        self.name_col = name_col
        self.max_match = max_match



def test():
    """
    Uses the above code to generate a simple test match-table.

    """
                     
