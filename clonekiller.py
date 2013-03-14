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

    # crude copy: `ft` is `flagged_table` 
    ft = table.where(table.RA > 0)
    
    ft.sort('RA')

    # convert max_offset to radians
    max_offsetr = np.radians(max_offset / 3600)

    clone = np.zeros(len(ft),dtype=np.int64)

    q = 0

    for i in range(1,len(ft)):

        # compare Dec to the previous source
        if np.abs(ft.DEC[i] - ft.DEC[i-1]) < max_offsetr:
            print np.degrees(np.abs(ft.DEC[i] - ft.DEC[i-1]))*3600
            print ("I think sources %s and %s are clones!" % 
                   (ft.SOURCEID[i-1], ft.SOURCEID[i]) ) 
            print ("(that's ONCvar %s and ONCvar %s)" %  
                   (ft.ONCvar_ID[i-1], ft.ONCvar_ID[i]))

            # if it's a clone, check if the previous guy was a clone
            if clone[i-1] != 0:
                clone[i] = clone[i-1]
            else:
                clone[i] = ft.SOURCEID[i-1]


    # now add the clone column
    ft.add_column("clone", clone)

    flagged_table = ft
    
    return flagged_table
