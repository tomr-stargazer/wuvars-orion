"""

This is a script for making images & figures for Orion that require APLpy.

Each figure (or, sometimes, group of closely related figures) is generated
by its own function, so that you don't HAVE to regenerate them all at the same
time if you only want one.

"""

import os

from figure_maker import *

import aplpy

dropbox_bo_images = os.path.expanduser("~/Dropbox/Bo_Tom/images/")

def figure_1(dots=True, rect=True):
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

    pass
 
