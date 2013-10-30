"""
This is a quick script to output the center coordinates, 
min and max coordinates, etc, of our field, in both decimal
and sexagesimal.

"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

try:
    import coords
except ImportError:
    import astrolib.coords as coords

from official_star_counter import minimum

max_ra = minimum.RA.max()
min_ra = minimum.RA.min()
max_dec = minimum.DEC.max()
min_dec = minimum.DEC.min()

center_ra = (max_ra+min_ra)/2
center_dec = (max_dec+min_dec)/2 

center_coordinates = coords.Position((center_ra, center_dec),
                                     units='radians')

northeast_corner_coordinates = coords.Position((max_ra, max_dec),
                                               units='radians')
southwest_corner_coordinates = coords.Position((min_ra, min_dec),
                                               units='radians')

def plot_minimum_sources():

    fig = plt.figure()

    plt.plot(np.degrees(minimum.RA), np.degrees(minimum.DEC), 'k.')

    return fig

if __name__ == '__main__':

    print " === Decimal ==="

    print "Center coordinates:"
    print center_coordinates.dd()

    print "North boundary:"
    print northeast_corner_coordinates.dd()[1]
    print "South boundary:"
    print southwest_corner_coordinates.dd()[1]
    
    print "East boundary:"
    print northeast_corner_coordinates.dd()[0]
    print "West boundary:"
    print southwest_corner_coordinates.dd()[0]

    print ""
    print " === Sexagesimal ==="
    print "Center coordinates:"
    print center_coordinates.hmsdms()

    print "North boundary:"
    print northeast_corner_coordinates.hmsdms().split()[1]
    print "South boundary:"
    print southwest_corner_coordinates.hmsdms().split()[1]
    
    print "East boundary:"
    print northeast_corner_coordinates.hmsdms().split()[0]
    print "West boundary:"
    print southwest_corner_coordinates.hmsdms().split()[0]

