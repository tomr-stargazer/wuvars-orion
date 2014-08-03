"""
aatau_analysis.py



"""


from __future__ import division

import os

import numpy as np
import matplotlib.pyplot as plt
import astropy.table

import plot3
from variables_data_filterer import source_photometry
from tablemate_comparisons import ukvar_spread, ukvar_periods
from table_maker import make_megeath_class_column

megeath_class_column = make_megeath_class_column()

path = os.path.expanduser("~/Dropbox/Bo_Tom/aux_catalogs/dipper_counting/")

aatau_ids = np.sort(np.loadtxt(path+'periodic_sub20days_AATau_analogs.txt'))

# this only works if ukvar_spread['UKvar_ID'] is monotonically increasing
aatau_spread = ukvar_spread.where(np.in1d(ukvar_spread['UKvar_ID'], aatau_ids))
aatau_periods = ukvar_periods[np.in1d(ukvar_spread['UKvar_ID'], aatau_ids)]
aatau_classes = megeath_class_column[np.in1d(ukvar_spread['UKvar_ID'], aatau_ids)]


# things to compute:
# 1. number of AA Taus, versus total number of periodic variables

num_aataus = len(aatau_spread)
num_variables = len(ukvar_spread)
num_periodics = np.sum(~np.isnan(ukvar_periods))

print "There are {0} total variables, and {1} total periodic variables.".format(num_variables, num_periodics)
print "Of these, {0} are AA Taus (periodic 'dippers').".format(num_aataus)
print "This is {0:.1f}% of all variables and {1:.1f}% of periodic variables.".format(num_aataus/num_variables*100, num_aataus/num_periodics*100)
print ""

# 2. number of Disked AA Taus, versus total number of disked variables / disked periodics

num_aatau_protostars = np.sum( aatau_classes == 'P' )
num_aatau_disks = np.sum( aatau_classes == 'D' )
num_aatau_nondisks = np.sum( aatau_classes == 'ND' )
num_aatau_unknownclass = np.sum( aatau_classes == 'na' )

print "Class distribution of AA Taus:"
print '{0} class "P"'.format(num_aatau_protostars)
print '{0} class "D"'.format(num_aatau_disks)
print '{0} class "ND"'.format(num_aatau_nondisks)
print '{0} unknown class'.format(num_aatau_unknownclass)
print ""

num_disks = np.sum( megeath_class_column == 'D' )
num_periodic_disks = np.sum((megeath_class_column == 'D') & (~np.isnan(ukvar_periods)))

print "There are {0} disked stars, and {1} periodic disked stars.".format(num_disks, num_periodic_disks)
print "Thus {:.1f}% of all disked stars are of AA Tau type,\nand {:.1f}% of periodic disked stars are of AA Tau type".format(100*num_aatau_disks/num_disks, 100*num_aatau_disks/num_periodic_disks)

# 3. distribution of AA Tau periods, also versus "mass"
def aatau_period_plots():

	fig1 = plt.figure()

	plt.hist(aatau_periods, range=(2,20), bins=18)

	plt.xlabel("AA Tau period (days)")
	plt.title("Histogram of AA Tau periods")

	fig2 = plt.figure()

	plt.plot(aatau_periods, aatau_spread.k_medianr, 'ro')

	plt.gca().invert_yaxis()

	plt.xlabel("AA Tau period (days)")
	plt.ylabel("AA Tau $K$ mag")
	plt.title("Bright AA Taus have longer periods than faint AA Taus")

	return fig1, fig2


#4. color mag, color color
def aatau_colors():

	periods_less_than_10 = aatau_periods < 10

	fig1 = plt.figure()

	plt.scatter(aatau_spread.hmk_medianr[periods_less_than_10], aatau_spread.k_medianr[periods_less_than_10], 
		c=aatau_periods[periods_less_than_10], cmap='jet_r', vmin=2, vmax=10)
	plt.gca().invert_yaxis()

	plt.xlabel("AA Tau median $H-K$")
	plt.ylabel("AA Tau $K$ mag")

	plt.title("Color-mag diagram of AA Taus, colored by period")

	cbar = plt.colorbar()
	cbar.set_label(r"AA Tau period")


	return fig1
