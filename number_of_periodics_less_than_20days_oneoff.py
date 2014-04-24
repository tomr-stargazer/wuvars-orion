"""
How many periodic stars are being shown in Figure 12?

"""

from figure_maker import *

megeath_class_column = make_megeath_class_column()

def count_periodics_under(days=20):

	number_under_days = len(ukvar_periods[(megeath_class_column != 'na') & 
		                                  (ukvar_periods <= days)])

	return number_under_days