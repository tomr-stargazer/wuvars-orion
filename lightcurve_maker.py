"""
A script to generate some custom lightcurves for the M42 paper using plot4.

"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from plot4 import lc_and_phase_and_colors, multi_lc_phase_colors, multi_lc_colors
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
		ax_phase = axes_dict['phase']
		ax_jhk = axes_dict['jhk']

		print "Doing thing with ONCvar {0}!".format(name)

		ax_phase.text(0.1, 0.1, "ONCvar {0}".format(stardata.name), transform=ax_phase.transAxes, fontsize='small')
		ax_phase.text(0.6, 0.1, "P = {0:.2f} d".format(period), transform=ax_phase.transAxes, fontsize='small')

		ax_jhk.set_xlim(0,1.5)
		ax_jhk.set_ylim(0,2)

		aafig.canvas.draw()
	return aafig

def longterm_nonperiodic_tenpanel(**kwargs):

	# compiled on 10 Sep 2010
	longnononcvar_ids = sorted([1030, 30, 910, 1156, 148, 177, 28, 313, 605, 705])

	longnonsourceids = [ukvar_spread['SOURCEID'][ukvar_spread['UKvar_ID'] == oncvar][0] for oncvar in longnononcvar_ids]
	longnonstardatas = [
    	OrionStarData(
	    	variables_photometry, sourceid, 
		    name='{}'.format(oncvar_id)) for sourceid, oncvar_id in zip(longnonsourceids, longnononcvar_ids)]

	bands = ['k']*10

	longnon_fig = multi_lc_colors(longnonstardatas, bands, **kwargs)

	for stardata, axes_dict in zip(longnon_fig.stardatas, longnon_fig.axes_dicts):

		name = stardata.name
		ax_jhk = axes_dict['jhk']
		ax_lc = axes_dict['lc']

		print "Doing thing with ONCvar {0}!".format(name)

		ax_lc.text(0.6, 0.8, "ONCvar {0}".format(stardata.name), transform=ax_lc.transAxes, fontsize='small')

		ax_jhk.set_xlim(0,1.5)
		ax_jhk.set_ylim(0,2)

		longnon_fig.canvas.draw()
	return longnon_fig

def dipper_nonperiodic_fivepanel(**kwargs):

	# compiled on 10 Sep 2010
	dipper_oncvar_ids = sorted([600, 165, 185, 423, 441])

	dipper_sourceids = [ukvar_spread['SOURCEID'][ukvar_spread['UKvar_ID'] == oncvar][0] for oncvar in dipper_oncvar_ids]
	dipper_stardatas = [
    	OrionStarData(
	    	variables_photometry, sourceid, 
		    name='{}'.format(oncvar_id)) for sourceid, oncvar_id in zip(dipper_sourceids, dipper_oncvar_ids)]

	bands = ['k']*len(dipper_oncvar_ids)

	dipper_fig = multi_lc_colors(dipper_stardatas, bands, **kwargs)

	for stardata, axes_dict in zip(dipper_fig.stardatas, dipper_fig.axes_dicts):

		name = stardata.name
		ax_jhk = axes_dict['jhk']
		ax_lc = axes_dict['lc']

		print "Doing thing with ONCvar {0}!".format(name)

		ax_lc.text(0.6, 0.1, "ONCvar {0}".format(stardata.name), transform=ax_lc.transAxes, fontsize='small')

		ax_jhk.set_xlim(0,1.5)
		ax_jhk.set_ylim(0,2)

		dipper_fig.canvas.draw()
	return dipper_fig


def seven_longperiod_variables_bo(**kwargs):

	sevenlong_oncvar_ids = [479, 149, 1226, 637, 802, 874, 665]
	offsets = [0.5, -0.35, 0.12, -0.1, 0.3, 0.05, -0.05]

	sevenlong_sourceids = [ukvar_spread['SOURCEID'][ukvar_spread['UKvar_ID'] == oncvar][0] for oncvar in sevenlong_oncvar_ids]
	# try:
	# 	sevenlong_periods = [ukvar_periods[ukvar_spread['UKvar_ID'] == oncvar][0] for oncvar in sevenlong_oncvar_ids]
	sevenlong_periods = [17.79, 36.4, 88.5, 42.5, 158.8, 75.16, 44.27]

	sevenlong_stardatas = [OrionStarData(variables_photometry, sourceid, name='{}'.format(oncvar_id)) for sourceid, oncvar_id in zip(sevenlong_sourceids, sevenlong_oncvar_ids)]

	bands = ['k']*7

	seven_fig = multi_lc_phase_colors(sevenlong_stardatas, bands, sevenlong_periods, offsets, **kwargs)

	for stardata, period, axes_dict in zip(seven_fig.stardatas, seven_fig.periods, seven_fig.axes_dicts):

		name = stardata.name 
		ax_phase = axes_dict['phase']
		ax_jhk = axes_dict['jhk']

		print "Doing thing with ONCvar {0}!".format(name)

		ax_phase.text(0.1, 0.8, "ONCvar {0}".format(stardata.name), transform=ax_phase.transAxes, fontsize='small')
		ax_phase.text(0.6, 0.8, "P = {0:.2f} d".format(period), transform=ax_phase.transAxes, fontsize='small')

		ax_jhk.set_xlim(0,2)
		ax_jhk.set_ylim(0,2.5)

		seven_fig.canvas.draw()
	return seven_fig

def seven_clean_rotators(**kwargs):
	rotator_oncvar_ids = [40, 359, 397, 906, 1068, 1091, 1165]
	offsets = [0.5, 0.2, 0.1, 0.5, 0, 0.1, 0]

	rotator_sourceids = [ukvar_spread['SOURCEID'][ukvar_spread['UKvar_ID'] == oncvar][0] for oncvar in rotator_oncvar_ids]
	rotator_periods = [ukvar_periods[ukvar_spread['UKvar_ID'] == oncvar][0] for oncvar in rotator_oncvar_ids]

	rotator_stardatas = [OrionStarData(variables_photometry, sourceid, name='{}'.format(oncvar_id)) for sourceid, oncvar_id in zip(rotator_sourceids, rotator_oncvar_ids)]

	bands = ['k']*len(rotator_oncvar_ids)

	rotator_fig = multi_lc_phase_colors(rotator_stardatas, bands, rotator_periods, offsets, **kwargs)

	for stardata, period, axes_dict in zip(rotator_fig.stardatas, rotator_fig.periods, rotator_fig.axes_dicts):

		name = stardata.name 
		ax_phase = axes_dict['phase']
		ax_jhk = axes_dict['jhk']

		print "Doing thing with ONCvar {0}!".format(name)

		ax_phase.text(0.1, 0.8, "ONCvar {0}".format(stardata.name), transform=ax_phase.transAxes, fontsize='small')
		ax_phase.text(0.6, 0.1, "P = {0:.2f} d".format(period), transform=ax_phase.transAxes, fontsize='small')

		ax_jhk.set_xlim(0,2)
		ax_jhk.set_ylim(0,2.5)

		rotator_fig.canvas.draw()
	return rotator_fig
