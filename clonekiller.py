"""
This is a module for detecting and removing "cloned" sources in WFCAM data.

A cloned source is one that has an identical (or identical modulo a few 
datapoints) lightcurve as another star, and more importnatly, is at the 
same physical location.

"""

def clone_flagger(table, max_offset=0.1):
    """
    Flags which sources in a table are clones of a previous source.

    Returns a version `table`, sorted by RA, with a new `clone` column.

    Parameters
    ----------
    table : atpy.Table
        Spreadsheet of info on WFCAM sources. One WFCAM-detected source
        per row. Must have RA, DEC columns in radians.
    max_offset : float, optional
        Maximum separation, in arcseconds, between two sources to be 
        considered "clones". Default 0.1.

    Returns
    -------
    flagged_table : atpy.Table
        Copy of `table` sorted by RA and with a new `clone` column.

    """

    
    
