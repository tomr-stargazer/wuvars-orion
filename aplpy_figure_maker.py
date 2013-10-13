"""

This is a script for making images & figures for Orion that require APLpy.

Each figure (or, sometimes, group of closely related figures) is generated
by its own function, so that you don't HAVE to regenerate them all at the same
time if you only want one.

"""

from __future__ import division
import os

from figure_maker import *

import aplpy

dropbox_bo_images = os.path.expanduser("~/Dropbox/Bo_Tom/images/")

def m42_map(xmarker_array=None, ymarker_array=None, rect=True, latex=True):
    """
    Shows our field on top of VISTA's great M42 image.

    Parameters
    ----------
    xmarker_array, ymarker_array : numpy.ndarrays
        X and Y coordinates (here, R.A. and Decl.) of the markers to plot
    rect : bool, optional
        Plot the rectangle demarcating our field?
    latex : bool, optional
        Use LaTeX to render the text and labels?

    Returns
    -------
    fig : aplpy.FITSFigure

    """

    fig = aplpy.FITSFigure(dropbox_bo_images+"slice.fits", north=True)

    fig.show_rgb(dropbox_bo_images+"eso1006a.jpg")

    center_of_box_ra = np.degrees(maxvars.RA.min() +
                                  maxvars.RA.max())/2
    center_of_box_dec= np.degrees(maxvars.DEC.min() +
                                  maxvars.DEC.max())/2

    width_of_box_ra = np.degrees(maxvars.RA.max() -
                                 maxvars.RA.min())
    width_of_box_dec = np.degrees(maxvars.DEC.max() -
                                  maxvars.DEC.min())

    fig.show_rectangles(center_of_box_ra, center_of_box_dec,
                        width_of_box_ra, width_of_box_dec,
                        color='y', lw=3)

    if xmarker_array != None and ymarker_array != None:
        fig.show_markers(xmarker_array, ymarker_array,
                         marker='+',edgecolor='w', s=40)

        fig.show_markers(xmarker_array, ymarker_array,
                         marker='o',edgecolor='r', s=2)

    northeast_corner = (np.degrees(maxvars.RA.max() + 0.001),
                        np.degrees(maxvars.DEC.max() + 0.001))

    southwest_corner = (np.degrees(maxvars.RA.min() - 0.001),
                        np.degrees(maxvars.DEC.min() - 0.001))

    px_northeast_corner = fig.world2pixel(northeast_corner[0], northeast_corner[1])
    px_southwest_corner = fig.world2pixel(southwest_corner[0], southwest_corner[1])
    
    plt.xlim(px_northeast_corner[0], px_southwest_corner[0])

    plt.ylim(px_southwest_corner[1], px_northeast_corner[1])

    if latex:
        fig.set_system_latex(True)

    return fig
 

def figure_1(**kwargs):

    return m42_map(np.degrees(ukvar_spread.RA), 
                   np.degrees(ukvar_spread.DEC))

def map_of_EBs(**kwargs):

    # define the EB coordinates
    previously_known_EB_tuples = [
        (83.7737916667,	-5.39836111111),
        (84.0247916667,	-5.01144444444),
        (83.841, -5.76902777777778),
        (83.6160416666667,	-5.69383333333333),
        (83.7964166666667,	-5.61422222222222),
        (83.8006083333333,	-5.52745833333333) ]
    previously_known_EB_ra = [x for (x,y) in previously_known_EB_tuples]
    previously_known_EB_dec = [y for (x,y) in previously_known_EB_tuples]

    too_bright_EB_tuples = [
        (83.8147916667,	-5.42058333333),
        (83.8156666667,	-5.38608333333),
        (83.825125,		-5.36816666667)]
    too_bright_EB_ra = [x for (x,y) in too_bright_EB_tuples]
    too_bright_EB_dec = [y for (x,y) in too_bright_EB_tuples]

    new_EB_tuples = [
        (83.50864084,		-5.29046598),
        (84.08421509,		-5.23937444),
        (84.2290583333333,	-4.97219638888889),
        (84.2247291666667,	-5.43198555555556)]        
    new_EB_ra = [x for (x,y) in new_EB_tuples]
    new_EB_dec = [y for (x,y) in new_EB_tuples]

    fig = m42_map(**kwargs)
    fig.show_grayscale()

    fig.show_markers(previously_known_EB_ra, previously_known_EB_dec, 
                     marker='o', edgecolor='w', facecolor='r', s=30)
    fig.show_markers(too_bright_EB_ra, too_bright_EB_dec, 
                     marker='o', edgecolor='w', facecolor='b', s=30)
    fig.show_markers(new_EB_ra, new_EB_dec, 
                     marker='*', edgecolor='w', facecolor='g', s=60)
    
    

    return fig

