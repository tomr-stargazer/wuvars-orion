"""
aatau_analysis.py



"""


from __future__ import division

import os

import numpy as np
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
# 2. number of Disked AA Taus, versus total number of disked variables / disked periodics
# 3. distribution of AA Tau periods, also versus mass
