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

def figure_1(dots=True, rect=True, latex=True):
    """
    Shows our field on top of VISTA's great M42 image.

    Parameters
    ----------
    dots : bool, optional
        Plot the markers where our variables live?
    rect : bool, optional
        Plot the rectangle demarcating our field?

    Returns
    -------
    fig : aplpy.FITSFigure

    """

    fig = aplpy.FITSFigure(dropbox_bo_images+"slice.fits", north=True)

    fig.show_rgb(dropbox_bo_images+"eso1006a.jpg")

    fig.show_markers(np.degrees(ukvar_spread.RA), 
                     np.degrees(ukvar_spread.DEC), 
                     marker='+',edgecolor='w', s=20)

    fig.show_markers(np.degrees(ukvar_spread.RA), 
                     np.degrees(ukvar_spread.DEC), 
                     marker='o',edgecolor='r', s=2)

    center_of_box_ra = np.degrees(ukvar_spread.RA.min() + ukvar_spread.RA.max())/2
    center_of_box_dec= np.degrees(ukvar_spread.DEC.min()+ ukvar_spread.DEC.max())/2

    width_of_box_ra = np.degrees(ukvar_spread.RA.max() - ukvar_spread.RA.min())
    width_of_box_dec = np.degrees(ukvar_spread.DEC.max() - ukvar_spread.DEC.min())

    fig.show_rectangles(center_of_box_ra, center_of_box_dec,
                        width_of_box_ra, width_of_box_dec,
                        color='y', lw=3)

    if latex:
        fig.set_system_latex(True)

    return fig
 
