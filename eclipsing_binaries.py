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

path = os.path.expanduser("~/Dropbox/Bo_Tom/data/")

eclipsing_binary_table = astropy.table.Table.read(
	path+'eclipsing_binaries.csv', format='ascii', delimiter=',')

# Choose the ones we numbered explicitly -- these are the only ones we have data for.
relevant_EB_table = eclipsing_binary_table[eclipsing_binary_table['index'].mask == False]

def make_lightcurves():

	figlist = []
	for sid, i in zip(relevant_EB_table['WFCAM SOURCEID'], range(len(relevant_EB_table))):

		lc_fig = plot3.graded_lc(source_photometry, sid, abridged=True, timecolor=True,
			name="ONCvar {0}: Eclipsing Binary #{1}".format(
				relevant_EB_table['ONCvar ID'][i], relevant_EB_table['index'][i]))

		figlist.append(lc_fig)

	return figlist


