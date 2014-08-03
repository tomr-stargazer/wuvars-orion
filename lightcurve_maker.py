"""
A script to generate some custom lightcurves for the M42 paper using plot4.

"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from plot4 import lc_and_phase_and_colors, multi_lc_phase_colors
from orion_plot import OrionStarData
from tablemate_comparisons import ukvar_spread, ukvar_periods
from variables_data_filterer import variables_photometry

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

def aatau_tenpanel(**kwargs):

	aatau_oncvar_ids = [130, 234, 295, 311, 334, 337, 371, 431, 553, 929]
	offsets = [-0.2, -0.15, 0.5, 0.25, 0, -0.25, 0.5, 0.3, 0.1, 0.1]

	aatau_sourceids = [ukvar_spread['SOURCEID'][ukvar_spread['UKvar_ID'] == oncvar][0] for oncvar in aatau_oncvar_ids]
	aatau_periods = [ukvar_periods[ukvar_spread['UKvar_ID'] == oncvar][0] for oncvar in aatau_oncvar_ids]

	aatau_stardatas = [OrionStarData(variables_photometry, sourceid, name='{}'.format(oncvar_id)) for sourceid, oncvar_id in zip(aatau_sourceids, aatau_oncvar_ids)]

	bands = ['k']*10

	aafig = multi_lc_phase_colors(aatau_stardatas, bands, aatau_periods, offsets, **kwargs)

	for stardata, period, axes_dict in zip(aafig.stardatas, aafig.periods, aafig.axes_dicts):

		name = stardata.name 
		ax = axes_dict['phase']

		print "Doing thing with ONCvar {0}!".format(name)

		ax.text(0.1, 0.1, "ONCvar {0}".format(stardata.name), transform=ax.transAxes, fontsize='small')
		ax.text(0.6, 0.1, "P = {0:.2f} d".format(period), transform=ax.transAxes, fontsize='small')

		aafig.canvas.draw()
	return aafig
