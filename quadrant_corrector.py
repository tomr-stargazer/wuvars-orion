"""
This is a Python module to correct 'bad' nights in the 
UKIRT Orion data, and perhaps other similar datasets.
It relies on the principle of finding nearby constant stars
to use for reference magnitudes on every night.

In particular, each star is compared to four reference stars, 
one located in each quadrant (NE, SE, SW, NW) for ease of computation
and to ensure that they enclose the given star.

"""

from __future__ import division

import numpy as np

import atpy
import coords

from helpers3 import band_cut

def quadrant_match( ra, dec, ref_table, max_match=600):
    """ 
    Matches a position to 4 reference stars that enclose the position.

    Parameters
    ----------
    ra, dec : float
        Right ascension and declination, in decimal degrees
    ref_table : atpy.Table
        Sub-table with 'spreadsheet' information that pertains 
        specifically to the region we're matching to.

    Returns
    -------
    sid_list : list of numpy.int64
        Source IDs of the four quadrant matches
    offset_list : list of float
        Offset, in arcseconds, of the four matches from target
    ra_list, dec_list : list of float
        Coordinates of the four matches.

    """
    

    delta = np.cos(np.abs(dec))
    boxsize = max_match / 3600.

    min_offset = -0.1 * np.ones_like(radd1)
    match      = -1   * np.ones_like(radd1).astype(int)

    counter = 1

    

def quadrant_corrector(data, j_constants, h_constants, k_constants):
    """
    Corrects magnitudes using a network of constant stars.

    Parameters
    ----------
    data : atpy.Table
        Table with UKIRT time-series photometry.
    j_constants, h_constants, k_constants : atpy.Table
        Table with 'spreadsheet' information on J, H, and K constants.
        Requires robust statistical information. 
        Must be pre-cleaned (we'll use all the constants you give us)

    Returns
    -------
    new_data : atpy.Table
        The corrected data table, with photometry corrected using the network.

    """

    # Make a copy of the data table 
    new_data = data.where(data.SOURCEID != 0)

    new_data.add_column

    # glue your set of constant lists together
    cdict = {'j':j_constants, 'h':h_constants, 'k':k_constants}
    
    for band in ['j', 'h', 'k']:
        
        # Grab the timestamps we'll be iterating over
        bdata = band_cut(data, band, max_flag=256)

        timestamp_list = list(set(list(bdata.MEANMJDOBS)))

        timestamp_list.sort()

        for date in timestamp_list:
            
            # first, grab the sourceids that are in this here night
            
            this_night = bdata.where(bdata.MEANMJDOBS == date)

            source_list = this_night.SOURCEID
            ra_list = this_night.RA
            dec_list = this_night.DEC
            
            # And also grab the constants that are in this here night!

            ref_phot = cdict[band].where(
                np.in1d(cdict[band].SOURCEID, source_list) )

            for s in source_list:
                
                # Find four nearby constants (one in each column)

                quad_match

                    

    night_list
