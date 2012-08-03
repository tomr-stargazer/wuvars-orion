"""
variability_map.py

This is a module that I intend to function as a way to make 
spatial visualizations of how stars vary over time.

"""


import numpy as np
import matplotlib.pyplot as plt

import atpy

from helpers3 import band_cut

def mapmaker(data, spreadsheet, band,  path, min_mag=17):
    """
    A function to make variability map movies.

    Produces only the PNGs required to make the movies. In order 
    to glue them together, manually run a command like:

    mencoder mf://*.png -mf fps=1:type=png -ovc copy -o k_movie_slow.avi
    
    to create a .avi video.

    Parameters
    ----------
    data : atpy.Table
        Table that contains all the photometry data.
    spreadsheet : atpy.Table
        Table that contains median photometry and stuff
    band : str {'j'|'h'|'k'}
        Which band to use.
    path : string
        Place to save to.

    """

    if not (len(band)==1 and type(band) is str):
        raise(ValueError)
    
    col = band.upper()+"APERMAG3"
    bandmean = band.lower()+"_meanr"
    pperrbits = band.upper()+"PPERRBITS"

    # First, let's make the list of dates that we are iterating through.
    date_list = list(set(list(np.trunc(data.MEANMJDOBS))))

    date_list.sort()

    # Now we iterate over our date list.

    for night in date_list:
        
        # Grab this night's photometry that corresponds to the input constant
        # star list.
        
        # relevant data
        rdata = band_cut(data, band, max_flag=256)
        
        this_nights_phot = rdata.where( 
            (np.trunc(rdata.MEANMJDOBS) == night) &
            (np.in1d(rdata.SOURCEID, spreadsheet.SOURCEID)) &
            (rdata.data[col] < min_mag))

        # Grab the spreadsheet info that corresponds exactly to this night's 
        # stars. ("reference photometry")

        ref_phot = spreadsheet.where(
            np.in1d(spreadsheet.SOURCEID, this_nights_phot.SOURCEID) )

        print "For night %s:" % night
        print len(this_nights_phot), len(ref_phot)
        
        # Now compute the deviation for each star.
        # (I'd love to do this in an array-based way, but some stars have 
        # two observations per night, and that breaks my array-based method...)
        
        deviation = np.zeros_like( ref_phot.data[bandmean] )
        
        for i in range(len(deviation)):
            
            this_stars_phot = this_nights_phot.where(
                this_nights_phot.SOURCEID == ref_phot.SOURCEID[i])
            
            deviation[i] = (
                this_stars_phot.data[col][0] - ref_phot.data[bandmean][i])

        try:
            fig = plt.figure()
            
            plt.scatter(np.degrees(ref_phot.RA), np.degrees(ref_phot.DEC), 
                        s = (19 - ref_phot.data[bandmean])**2,
                        c = deviation, cmap='RdBu_r', vmin=-0.15, vmax=0.15)
            
            
            cbar = plt.colorbar()
            cbar.set_label("Deviation from mean magnitude")
            cbar.ax.invert_yaxis()
            fig.gca().invert_xaxis()
            fig.gca().set_aspect('equal')
            
            plt.xlabel("Right Ascension (degrees)")
            plt.ylabel("Declination (degrees)")
            plt.xlim(84.3, 83.2)
            plt.ylim(-5.95, -4.9)

            plt.title("Night: MJD = %s (%d since 01/01/2000)" % 
                      (str(night), night - 51544))

        
            plt.savefig(path+'%s.png' % str(night))
            plt.close()

        except ValueError:
            continue

#        if night > 54030.0:

#            break

def deviation_plot(data, spreadsheet, band,  path, min_mag=17):
    """
    Plots the deviation of each constant star as a function of magnitude.
    
    Parameters
    ----------
    data : atpy.Table
        Table that contains all the photometry data.
    spreadsheet : atpy.Table
        Table that contains median photometry and stuff
    band : str {'j'|'h'|'k'}
        Which band to use.
    path : string
        Place to save to.

    """

