"""
This is a module that contains software to 'cleanse' bad nights
from a UKIRT time-series dataset. 

It currently relies on the output of 
"variability_map.count_constants_calc_ratio()" and is meant to create 
tables that can feed into anything that uses helpers3.py
(such as plot3, spread3, etc.).

"""

import numpy as np


def null_cleanser( data, nights, j_ratio, h_ratio, k_ratio, threshold=0.9,
                   null=np.double(-9.99999488e+08)):
    """
    Cleans data by nullifying.
    
    For any night with a quality lower than `threshold` in a given band,
    this function replaces all photometry in that band with `null`.

    Parameters
    ----------
    data : atpy.Table
        Table that contains all the photometry data.
    nights : np.ndarray
        Array of nights that have data.
    j_ratio, h_ratio, k_ratio : np.ndarray
        Quality ratios (0.0 - 1.0) for each night at J, H, and K bands.
    threshold : float, optional
        Data below this threshold are cleansed by nullification.
    null : float, optional
        What value to use as a 'null' when cleansing data.
        Default value -9.99999e+08 (as used by WSA).


    Returns
    -------
    cleansed_data : atpy.Table
        Table with bad data nullified and ready to go.

    """
    
    # Make a copy of the data table
    cleansed_data = data.where(data.SOURCEID != 0)

    rdict =  {'j':j_ratio, 'h':h_ratio, 'k':k_ratio}

    for band in ['j', 'h', 'k']:

        col = band.upper()+"APERMAG3"

        for i in range(len(nights)):
       
            if rdict[band][i] < threshold:
                
                # print len(cleansed_data.data[col][ 
                #     np.trunc(cleansed_data.MEANMJDOBS) == nights[i] ])

                # print np.max(cleansed_data.data[col][ 
                #     np.trunc(cleansed_data.MEANMJDOBS) == nights[i] ])
                cleansed_data.data[col][ 
                    np.trunc(cleansed_data.MEANMJDOBS) == nights[i] ] = null

                # print np.max(cleansed_data.data[col][ 
                #     np.trunc(cleansed_data.MEANMJDOBS) == nights[i] ])

                # return
                
                print( "nullified night %d %s band (quality: %.2f)" % 
                       (nights[i], band.upper(), rdict[band][i]) )

    return cleansed_data


def flag_cleanser( data, nights, j_ratio, h_ratio, k_ratio, threshold=0.9 ):
    """
    Cleans data by flagging. Not yet implemented.
    
    """
    pass


def null_cleanser_grader(data, timestamps, j_ratio, h_ratio, k_ratio, 
                         threshold=0.9, null=np.double(-9.99999488e+08)):
    """
    Cleans data by nullifying, and appends quality grades onto data.
    
    For any exposure with a quality lower than `threshold` in a given band,
    this function replaces all photometry in that band with `null`.
    Also, the data is given three new columns: 
    "JGRADE", "HGRADE", and "KGRADE", which  describe a 
    given night's quality at these bands.

    Operates on individual exposure timestamps rather than nights, 
    so this function relies on the output of 
    "variability_map.exposure_grader()"

    Parameters
    ----------
    data : atpy.Table
        Table that contains all the photometry data.
    timestamps : np.ndarray
        Array of timestamps corresponding to exposure times.
    j_ratio, h_ratio, k_ratio : np.ndarray
        Quality ratios (0.0 - 1.0) for each night at J, H, and K bands.
    threshold : float, optional
        Data below this threshold are cleansed by nullification.
    null : float, optional
        What value to use as a 'null' when cleansing data.
        Default value -9.99999e+08 (as used by WSA).


    Returns
    -------
    cleansed_data : atpy.Table
        Table with bad data nullified and all data "graded"
        using new columns JGRADE, HGRADE, KGRADE.

    """
    
    # Make a copy of the data table
    cleansed_data = data.where(data.SOURCEID != 0)

    # Add columns to it!
    jgrade = -1. * np.ones_like(cleansed_data.JAPERMAG3)
    hgrade = -1. * np.ones_like(jgrade)
    kgrade = -1. * np.ones_like(jgrade)

    cleansed_data.add_column("JGRADE", jgrade)
    cleansed_data.add_column("HGRADE", hgrade)
    cleansed_data.add_column("KGRADE", kgrade)

    rdict =  {'j':j_ratio, 'h':h_ratio, 'k':k_ratio}

    for band in ['j', 'h', 'k']:

        col = band.upper()+"APERMAG3"
        grade = band.upper()+"GRADE"

        for i in range(len(timestamps)):

            # first, assign tonight's grade to all the data here
            
            cleansed_data.data[grade][
                cleansed_data.MEANMJDOBS == timestamps[i]] = rdict[band][i]

            if rdict[band][i] < threshold:

                # print len(cleansed_data.data[col][ 
                #     (cleansed_data.MEANMJDOBS) == timestamps[i] ])

                # print np.max(cleansed_data.data[col][ 
                #     (cleansed_data.MEANMJDOBS) == timestamps[i] ])
                cleansed_data.data[col][ 
                    cleansed_data.MEANMJDOBS == timestamps[i] ] = null

                # print np.max(cleansed_data.data[col][ 
                #     (cleansed_data.MEANMJDOBS) == timestamps[i] ])

                # return

                print( "nullified timestamp %f %s band (quality: %.2f)" % 
                       (timestamps[i], band.upper(), rdict[band][i]) )

    return cleansed_data
