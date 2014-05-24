"""
A script to generate some custom lightcurves for the M42 paper using plot4.

"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from plot4 import phase_axes_with_info, lightcurve_axes_with_info, colorcolor_axes, colormag_axes
from orion_plot import OrionStarData
from tablemate_comparisons import ukvar_spread, ukvar_periods
from variables_data_filterer import variables_photometry

def lc_and_phase_and_colors(stardata, period=None, timecolor=True, custom_xlabel=False, offset=0):
    """
    Generates an eight-panel lightcurve: phase-folded, straight, and color info.

    """

    # kwargs defaulting over
    time_cmap = 'jet'
    color_slope = False
    d_cmap={'j':'Blues', 'h': 'Greens', 'k': 'Reds'}

    if timecolor is True:
        colorscale='date'
    else:
        colorscale='grade'

    stretch_factor = 1.575

    fig = plt.figure(figsize = (10*stretch_factor, 6), dpi=80, facecolor='w', edgecolor='k')

    bottom = 0.1
    height = .25
    left = 0.075 / stretch_factor
    width = 0.5 / stretch_factor

    ax_k_lc = fig.add_axes( (left+(left+width), bottom, width, height) )
    ax_h_lc = fig.add_axes( (left+(left+width), bottom+.3, width, height), sharex=ax_k_lc )
    ax_j_lc = fig.add_axes( (left+(left+width), bottom+.6, width, height), sharex=ax_k_lc )

    ax_k_phase = fig.add_axes( (left, bottom, width, height) )
    ax_h_phase = fig.add_axes( (left, bottom+.3, width, height), sharex=ax_k_phase )
    ax_j_phase = fig.add_axes( (left, bottom+.6, width, height), sharex=ax_k_phase )

    color_height = 0.375
    color_left = 0.65 / stretch_factor + (left+width)
    color_width = 0.3 / stretch_factor

    ax_jhk = fig.add_axes( (color_left, bottom, color_width, color_height) )
    ax_khk = fig.add_axes( (color_left, bottom+.475, color_width, color_height) )

    d_ax_lc = {'j': ax_j_lc, 'h': ax_h_lc, 'k': ax_k_lc}
    d_ax_phase = {'j': ax_j_phase, 'h': ax_h_phase, 'k': ax_k_phase}

    if timecolor:
        d_cmap = {'j': time_cmap, 'h': time_cmap, 'k': time_cmap}
    elif type(d_cmap) is str:
        d_cmap = {'j': d_cmap, 'h': d_cmap, 'k': d_cmap}
    elif type(d_cmap) is not dict:
        d_cmap = {'j': d_cmap[0], 'h': d_cmap[1], 'k': d_cmap[2]}

    color_vmin = stardata.min_date
    color_vmax = stardata.max_date 

    if timecolor:
        vmin = color_vmin
        vmax = color_vmax
    else:
        vmin = 0.8
        vmax = 1

    for band in ['j', 'h', 'k']:
        lightcurve_axes_with_info(stardata, band, d_ax_lc[band], colorscale, 
                                  cmap=d_cmap[band], vmin=vmin, vmax=vmax)

        phase_axes_with_info(stardata, band, period, d_ax_phase[band], colorscale, 
                                  cmap=d_cmap[band], vmin=vmin, vmax=vmax, offset=offset)

    colorcolor_axes(stardata, ax_jhk, colorscale, cmap='jet', vmin=vmin, vmax=vmax,
                    color_slope=color_slope)
    colormag_axes(stardata, 'khk', ax_khk, colorscale, cmap='jet', vmin=vmin, vmax=vmax,
                  color_slope=color_slope)

    # Hide the bad labels...
    plt.setp(ax_j_lc.get_xticklabels(), visible=False)
    plt.setp(ax_h_lc.get_xticklabels(), visible=False)
    plt.setp(ax_j_phase.get_xticklabels(), visible=False)
    plt.setp(ax_h_phase.get_xticklabels(), visible=False)

    # Label stuff
    if custom_xlabel:
        ax_k_lc.set_xlabel( custom_xlabel )
    else:
        ax_k_lc.set_xlabel( "Time (MJD - %.1f)" % stardata.date_offset )

    ax_k_phase.set_xlabel("Phase (Period = {0:.4} days)".format(period))        

    ax_j_phase.set_ylabel( "J",{'rotation':'horizontal', 'fontsize':'large'} )
    ax_h_phase.set_ylabel( "H",{'rotation':'horizontal', 'fontsize':'large'} )
    ax_k_phase.set_ylabel( "K",{'rotation':'horizontal', 'fontsize':'large'} )

    ax_jhk.set_xlabel( "H-K" )
    ax_jhk.set_ylabel( "J-H")#, {'rotation':'horizontal'})
    ax_khk.set_xlabel( "H-K" )
    ax_khk.set_ylabel( "K")#, {'rotation':'horizontal'})

    fig.ax_k_lc = ax_k_lc
    fig.ax_h_lc = ax_h_lc
    fig.ax_j_lc = ax_j_lc

    fig.ax_k_phase = ax_k_phase
    fig.ax_h_phase = ax_h_phase
    fig.ax_j_phase = ax_j_phase


    fig.ax_jhk = ax_jhk
    fig.ax_khk = ax_khk

    return fig

def eightpanel_by_oncvar(oncvar, period=None, **kwargs):
	""" 
	Makes a lc_and_phase_and_colors plot 'smartly' based on an input ONCvar ID.

	"""

	sourceid = ukvar_spread['SOURCEID'][ukvar_spread['UKvar_ID'] == oncvar][0]

	if period is None:
		period = ukvar_periods[ukvar_spread['UKvar_ID'] == oncvar][0]

	stardata = OrionStarData(variables_photometry, sourceid)

	return lc_and_phase_and_colors(stardata, period, **kwargs)

def eightpanel_149():
	return eightpanel_by_oncvar(149, period=36.403, offset=0.65)

def eightpanel_479():
	return eightpanel_by_oncvar(479, period=17.786, offset=0.5)

def eightpanel_1226():
	return eightpanel_by_oncvar(1226, period=88.496, offset=0.1)

def eightpanel_957():
	return eightpanel_by_oncvar(957, offset=0.25)
