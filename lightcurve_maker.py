"""
A script to generate some custom lightcurves for the M42 paper using plot4.

"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from plot4 import lc_and_phase_and_colors
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
