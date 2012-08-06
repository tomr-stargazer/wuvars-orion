"""
This is a Python module to correct 'bad' nights in the 
UKIRT Orion data, and perhaps other similar datasets.
It relies on the principle of finding nearby constant stars
to use for reference magnitudes on every night.

In particular, each star is compared to four reference stars, 
one located in each quadrant (NE, SE, SW, NW) for ease of computation
and to ensure that they enclose the given star.

Created 3 August 2012 by Tom Rice (t.rice90@gmail.com).

"""

from __future__ import division

import numpy as np
from numpy import where
from numpy import intersect1d as sect

import atpy
import coords

from helpers3 import band_cut

def magnitude_adjustment( deviation_list, offset_list ):
    """
    Computes the magnitude correction for a given star.

    Parameters
    ----------
    deviation_list : list of float
        Deviations of the surrounding constant stars. Length 1-4.
    offset_list : list of float
        Offsets between surrounding constant stars and target star.
        Length 1-4 (matches `deviation_list`).

    Returns
    -------
    adjustment : float
        The adjustment to add to the uncorrected target magnitude value.

    """
    
    if len(deviation_list) != len(offset_list):
        raise ValueError("Arguments must be same length")

    deviation_list = np.array(deviation_list)
    offset_list = np.array(offset_list)
    
    adjustment = ( len(deviation_list) * np.sum(offset_list * deviation_list) / 
                   (4 * np.sum(offset_list)) )

    return adjustment


def quadrant_match( ra, dec, ref_table, max_match=600):
    """ 
    Matches a target to 4 reference stars that enclose that target.

    Much of this code is inspired by "match.py", especially from
    the function `core_match()`.

    Parameters
    ----------
    ra, dec : float
        Right ascension and declination of target, in decimal degrees
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
        Coordinates of the four matches, in decimal degrees.

    """
    
    # Loading up some useful variables
    delta = np.cos(np.radians(np.abs(dec)))
    boxsize = max_match / 3600.

#    min_offset = -0.1 * np.ones_like(radd1)
#    match      = -1   * np.ones_like(radd1).astype(int)

    const_ra = np.degrees(ref_table.RA)
    const_dec =np.degrees(ref_table.DEC) 

    # Let's make a data structure where we can keep the results of our matches.    
    sid_list = []
    offset_list = []
    ra_list = []
    dec_list = []
    
    p1 = coords.Position( (ra, dec), units='deg')

    # Quadrants:
    #  4 | 1
    #  --+--
    #  3 | 2
    #
    #  RA ->

    #    all quadrants:
    #    w1 = where(const_ra < ra + boxsize/delta)[0]
    #    w2 = where(const_ra > ra - boxsize/delta)[0]
    #    w3 = where(const_dec < dec + boxsize)[0]
    #    w4 = where(const_dec > dec - boxsize)[0]

    # first quadrant

    a_list = [0, 0, -boxsize/delta, -boxsize/delta]
    b_list = [boxsize/delta, boxsize/delta, 0, 0]
    c_list = [0, -boxsize, -boxsize, 0]
    d_list = [boxsize, 0, 0, boxsize]
    
    for a, b, c, d, q in zip(a_list, b_list, 
                             c_list, d_list, range(1,len(a_list)+1)):

        w1 = where(const_ra < ra + b)[0]
        w2 = where(const_ra > ra + a)[0]
        w3 = where(const_dec < dec + d)[0]
        w4 = where(const_dec > dec + c)[0]

        # Let's slice a box around our source
        box = sect(sect(w1,w2),sect(w3,w4))

        print "quadrant", q, ": ", len(box), " constants"

        # Now let's extract all the sources within "box" 
        # and calculate offsets to all of them

        offset = -1. * np.ones_like(const_ra[box])
        if offset.size != 0:
            for s2 in range(len(offset)):
                p2 = coords.Position( (const_ra[box][s2], const_dec[box][s2])
                                      ,  units = 'deg')

                offset[s2] = p1.angsep(p2).arcsec()

                # then we don't care! We want to find one star in each quadrant,
                # so you better do some slicing.


            print offset.min(), max_match
            if offset.min() < max_match:
                # min_offset[s1] = offset.min()
                offset_list.append(offset.min())
            
                match = box[where(offset == offset.min() )][0]

                sid_list.append( ref_table.SOURCEID[match] )
                ra_list.append( np.degrees(ref_table.RA[match]) )
                dec_list.append( np.degrees(ref_table.DEC[match]) )
            
                #            vprint( "Source %d: Matched with %f arcsec" \
#                        % (counter, offset.min() ) )
            else:
                print "match failure?"
                #            vprint( "Source %d: Failed to match" % counter)
                pass

    print offset_list
    return sid_list, offset_list, ra_list, dec_list

    

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

#    new_data.add_column

    # glue your set of constant lists together
    cdict = {'j':j_constants, 'h':h_constants, 'k':k_constants}
    
    for band in ['j', 'h', 'k']:
        
        # Grab the timestamps we'll be iterating over
        bdata = band_cut(data, band, max_flag=256)

        col = band.upper()+"APERMAG3"
        bandmean = band.lower()+"_meanr"


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

            for s, ra, dec in zip(source_list, ra_list, dec_list):
                
                # Find four nearby constants (one in each column)

                (sid_list, offset_list, 
                 ra_list, dec_list) = quadrant_match(
                    np.degrees(ra), np.degrees(dec), ref_phot,
                    max_match=600)
#                print offset_list, "sup"

                # Get the deviation of each constant
                 
                deviation = []
                for sid in sid_list:
                    this_stars_phot = this_night.where(
                        this_night.SOURCEID == sid)
                    this_stars_avg = ref_phot.where(
                        ref_phot.SOURCEID == sid)
            
                    deviation.append(this_stars_phot.data[col][0] - 
                                     this_stars_avg.data[bandmean][0])


                # Calculate the relevant offset

                adjustment = magnitude_adjustment(deviation, offset_list)

                # Apply the offset to our working table

                new_data.data[col][(new_data.SOURCEID == s) & 
                                   (new_data.MEANMJDOBS == date)] += adjustment
                
                print "Adjusted star %d by %f mag on night %d" % \
                    (s, adjustment, date)
                
                break

                    

    return new_data
