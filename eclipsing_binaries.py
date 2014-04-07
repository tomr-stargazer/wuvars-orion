"""
eclipsing_binaries.py

Some code in response to Bo's requests on eclipsing binaries.

"""

from __future__ import division

import os

import numpy as np
import astropy.table

import plot3
from variables_data_filterer import source_photometry
from tablemate_comparisons import ukvar_spread

path = os.path.expanduser("~/Dropbox/Bo_Tom/data/")

eclipsing_binary_table = astropy.table.Table.read(
	path+'eclipsing_binaries.csv', format='ascii', delimiter=',')

# Choose the ones we numbered explicitly -- these are the only ones we have data for.
relevant_EB_table = eclipsing_binary_table[eclipsing_binary_table['index'].mask == False]

# Make sure I didn't screw up the ONCvar IDs

for row in relevant_EB_table:
	assert row['ONCvar ID'] == ukvar_spread.UKvar_ID[ukvar_spread.SOURCEID == row['WFCAM SOURCEID']]

def make_lightcurves():

	figlist = []
	for sid, i in zip(relevant_EB_table['WFCAM SOURCEID'], range(len(relevant_EB_table))):

		lc_fig = plot3.graded_lc(source_photometry, sid, abridged=True, timecolor=True,
			name="ONCvar {0}: Eclipsing Binary #{1}".format(
				relevant_EB_table['ONCvar ID'][i], relevant_EB_table['index'][i]))

		figlist.append(lc_fig)

	return figlist

# JHK mag columns -- match our SOURCEIDs to ukvar_spread
bool_array = np.in1d(ukvar_spread.SOURCEID, relevant_EB_table['WFCAM SOURCEID'].data.data)
indices = np.where(bool_array)[0]

indices_sorted_by_sourceid = indices[np.argsort(ukvar_spread.SOURCEID[indices])]
indices_sorted_by_EB_number = indices_sorted_by_sourceid[
	np.argsort( relevant_EB_table['index'].data.data[ # sort the EB numbers by SOURCEID and then get the inverse sort order
		np.argsort(relevant_EB_table['WFCAM SOURCEID'])]     )]

sourceid_column = ukvar_spread.SOURCEID[indices_sorted_by_EB_number]

# make sure the sort went properly
assert len(relevant_EB_table) == len(sourceid_column)
for row, sid in zip(relevant_EB_table, sourceid_column):
	assert row['WFCAM SOURCEID'] == sid

j_column = ukvar_spread.j_meanr[indices_sorted_by_EB_number]
h_column = ukvar_spread.h_meanr[indices_sorted_by_EB_number]
k_column = ukvar_spread.k_meanr[indices_sorted_by_EB_number]

jmh_column = ukvar_spread.jmh_meanr[indices_sorted_by_EB_number]
hmk_column = ukvar_spread.hmk_meanr[indices_sorted_by_EB_number]