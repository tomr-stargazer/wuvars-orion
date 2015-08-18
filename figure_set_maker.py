"""
Makes figures for the AJ FigureSet.

"""

from __future__ import division

import numpy as np
import matplotlib

from plot4 import (lc_and_phase_and_colors, 
                   multi_lc_phase_colors, 
                   multi_lc_colors, basic_lc, StarData)
from orion_plot import OrionStarData

from variables_data_filterer import variables_photometry, source_photometry
from tablemate_comparisons import ukvar_spread, ukvar_periods

from lightcurve_maker import orion_cmap, fivepanel_by_oncvar


def figureset_page(oncvar_id):
    """ Creates a FigureSet page for a given star. """

    fig = fivepanel_by_oncvar(oncvar_id)

    # first: get the plot to conform nicely

    # parameters derived from ONCvar 1, interactively
    canonical_xticks = np.array([  0,  50, 100, 150, 187, 218, 268, 318])
    canonical_xtick_labels = ['0', '50', '100', '150', '391', '754', '804', '854']

    fig.ax_k.set_xlim(-4, 363)
    fig.ax_k.set_xticks(canonical_xticks)
    fig.ax_k.set_xticklabels(canonical_xtick_labels)

    # second: get text on the page in a nice sensible way

    identifier_string = 'Identifier: ONCvar {0}'.format(oncvar_id)

    period = ukvar_periods[ukvar_spread.UKvar_ID == oncvar_id][0]
    if np.isnan(period):
        period_fragment = 'None'
    else:
        period_fragment = '{0:.3f} days'.format(period)

    ra = 111 # placeholder
    dec = 222 # placeholder
    
    coordinates_string = r'Coordinates: $\alpha$ {0}, $\delta$ {1}'.format(ra, dec)
    period_string = 'Period: {0}'.format(period_fragment)
    quality_number = 2
    quality_dict = {0: 'all bands compromised',
                    1: '1-2 bands compromised',
                    2: 'no bands compromised'}
    quality_string = 'Quality Class: Q={0} ({1})'.format(quality_number, quality_dict[quality_number])

    text_parameters = {'fontsize':18, 'family':'serif'}
    fig.text(0.05, -0.06, identifier_string, **text_parameters)
    fig.text(0.05, -0.12, coordinates_string, **text_parameters)
    fig.text(0.05, -0.18, period_string, **text_parameters)
    fig.text(0.05, -0.24, quality_string, **text_parameters)

    # third: append this method hackishly (this avoids defining a Figure subclass)
    fig.savefig_tight = lambda filename: savefig_tight(fig, filename)

    fig.canvas.draw()
    return fig
    


def generate_mock_figureset_page():
    """ Allows us to test the figureset pages. """
    
    mock_id = 40 # this is a periodic star, well-behaved

    fig = figureset_page(mock_id)

    return fig


def save_mock_figureset_page():
    """ Allows us to test the figureset pages. """

    fig = generate_mock_figureset_page()

    fig.savefig_tight('test_blah.png')


def generate_all_figureset_pages():
    """ Generates all figureset pages."""
    pass


def savefig_tight(figure, filename):
    """ 
    A simple function to call the bbox_inches='tight' argument on savefig. 

    """

    if not type(figure) == matplotlib.figure.Figure:
        raise TypeError('`figure` must be an actual Figure')

    figure.savefig(filename, bbox_inches='tight')

