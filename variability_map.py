"""
variability_map.py

This is a module that I intend to function as a way to make 
spatial visualizations of how stars vary over time.

"""


import numpy as np
import atpy

def mapmaker(data, spreadsheet, path):
    """
    A function to make variability maps.

    Parameters
    ----------
    data : atpy.Table
        Table that contains all the photometry data.
    spreadsheet : atpy.Table
        Table that contains median photometry and stuff
    path : string
        Place to save to.

    """

    # First, let's make the list of dates that we are iterating through.
    date_list = 

    # Now we iterate over our date list.

    for night in date_list:
        
        # Grab this night's photometry that corresponds to the input constant
        # star list.
        this_nights_phot = data.where(

        
