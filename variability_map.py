"""
variability_map.py

This is a module that I intend to function as a way to make 
spatial visualizations of how stars vary over time.

"""

from __future__ import division

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

    if not (len(band)==1 and type(band) is str):
        raise(ValueError)
    
    col = band.upper()+"APERMAG3"
    bandmean = band.lower()+"_meanr"
    pperrbits = band.upper()+"PPERRBITS"

    colordict = {'k':'r', 'h':'g', 'j':'b'}

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
            
            plt.plot( ref_phot.data[bandmean], deviation, 
                      colordict[band.lower()]+'.')

            plt.plot( [5, 20], [0, 0], 'k--')
            plt.plot( [5, 20], [0.05, 0.05], 'k:')
            plt.plot( [5, 20], [-0.05, -0.05], 'k:')

            plt.xlabel("Mean %s magnitude" % band.upper())
            plt.ylabel("Deviation (mag)")

            plt.title("Night: MJD = %s (%d since 01/01/2000)" % 
                      (str(night), night - 51544))

            plt.xlim(11, min_mag+0.25)
            plt.ylim(-1,1)
            plt.gca().invert_yaxis()

            plt.savefig(path+'%s_dev.png' % str(night))
            plt.close()

#            if night > 54040.0:
#                break

        except:
            continue

    return None

def count_constants_calc_ratio(data, spreadsheet, band, min_mag=17):
    """
    Investigates the quality of nights by checking 
    a) how many constant stars are detected
    b) how many fall inside of, versus outside of, \pm .05 mag deviation

    Parameters
    ----------
    data : atpy.Table
        Table that contains all the photometry data.
    spreadsheet : atpy.Table
        Table that contains median photometry and stuff
    band : str {'j'|'h'|'k'}
        Which band to use.

    Returns
    -------
    date : np.ndarray
        Array of truncanted MJD dates corresponding to nights.
    n_const : np.ndarray
        Number of constant stars detected per night
    ratio : np.ndarray
        Ratio of (well-behaved)/(deviant) constants per night
      
    """
    
    if band.lower() not in ('j','h','k'):
        raise(ValueError)
    
    col = band.upper()+"APERMAG3"
    bandmean = band.lower()+"_meanr"
    pperrbits = band.upper()+"PPERRBITS"

    # First, let's make the list of dates that we are iterating through.
    date_list = list(set(list(np.trunc(data.MEANMJDOBS))))

    date_list.sort()

    print len(date_list)

    dates = np.array(date_list)
    n_const = np.zeros_like(dates, dtype='int')

    print len(n_const)
    ratio = np.zeros_like(dates, dtype='float')
    
    # Now we iterate over our date list.

    for night, i in zip(date_list, range(len(date_list))):
        
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
        
        for j in range(len(deviation)):
            
            this_stars_phot = this_nights_phot.where(
                this_nights_phot.SOURCEID == ref_phot.SOURCEID[j])
            
            deviation[j] = (
                this_stars_phot.data[col][0] - ref_phot.data[bandmean][j])

        # NOW count how many stars there are and the ratio that fall inside
        # versus outside the \pm .05 mag bands

        n_const[i] = len(deviation)

        goods = len( deviation[np.abs(deviation) < 0.05] )

        if n_const[i] > 0:
            ratio[i] = (goods / n_const[i])
        else:
            ratio[i] = 0
        
    return dates, n_const, ratio
