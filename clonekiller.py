"""
This is a module for detecting and removing "cloned" sources in WFCAM data.

A cloned source is one that has an identical (or identical modulo a few 
datapoints) lightcurve as another star, and more importantly, is at the 
same physical location.

"""

from __future__ import division

import numpy as np


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

    # crude copy
    flagged_table = table.where(table.RA > 0)
    
    flagged_table.sort('RA')

    # convert max_offset to radians
    max_offsetr = np.radians(max_offset / 3600)

    clone = np.zeros(len(flagged_table),dtype=np.int64)

    for i in range(1,len(flagged_table)):

        # compare Dec and RA to the previous source
        print np.degrees(np.abs(flagged_table.DEC[i] - flagged_table.DEC[i-1]))*3600
        if np.abs(flagged_table.DEC[i] - flagged_table.DEC[i-1]) < max_offsetr:
            print ("I think sources %s and %s are clones!" % 
                   (flagged_table.SOURCEID[i], flagged_table.SOURCEID[i-1]) ) 

        # if it's a clone, check if the previous guy was a clone

        # if that was the case, follow that back further
        
        # else, the first guy back was the clone we're assigning
        
        if i > 20: break
