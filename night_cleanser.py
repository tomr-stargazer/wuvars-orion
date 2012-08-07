"""
This is a module that contains software to 'cleanse' bad nights
from a UKIRT time-series dataset. 

It currently relies on the output of 
"variability_map.count_constants_calc_ratio()" and is meant to create 
tables that can feed into anything that uses helpers3.py
(such as plot3, spread3, etc.).

"""

import numpy as np


def null_cleanser( data, nights, j_ratio, h_ratio, k_ratio, threshold=0.9 ):
    """
    Cleans data by nullifying.

    For 

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


    Returns
    -------
    


    """

    return


def flag_cleanser( data, nights, j_ratio, h_ratio, k_ratio, threshold=0.9 ):
    """
    Cleans data by flagging. Not yet implemented.
    
    """
    pass
