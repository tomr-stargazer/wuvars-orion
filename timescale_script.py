"""
This is a script that analyzes color slope timescales.

It calls functions from color_slope_temporal_experiment.

"""

from color_slope_temporal_experiment import *

import matplotlib.pyplot as plt

delta_t_list = [5,10,20, 25, 30, 40, 50, 75, 100,1000]

def make_shuffle_dudes():

	non_shuffled = calculate_color_slope_ratios_versus_time_baseline(
		delta_t_list=delta_t_list, shuffle_dates=False)

	list_of_shuffle_dudes = []	

	for i in range(5):
		list_of_shuffle_dudes.append(
			calculate_color_slope_ratios_versus_time_baseline(
				delta_t_list=delta_t_list, shuffle_dates=True) )

	return list_of_shuffle_dudes, non_shuffled

def plot_shuffle_dudes(list_of_shuffle_dudes, non_shuffled):

	fig1 = plt.figure()

	plt.plot(non_shuffled.time_baseline, non_shuffled.n_positive_slope, 'r.')
	plt.plot(non_shuffled.time_baseline, non_shuffled.n_negative_slope, 'b.')

	fig2 = plt.figure()

	for shuffle in list_of_shuffle_dudes:

		plt.plot(shuffle.time_baseline, shuffle.n_positive_slope, 'r.')
		plt.plot(shuffle.time_baseline, shuffle.n_negative_slope, 'b.')

	return fig1, fig2


def do_it():
	list_of_shuffle_dudes, non_shuffled = make_shuffle_dudes()
	return plot_shuffle_dudes(list_of_shuffle_dudes, non_shuffled), list_of_shuffle_dudes, non_shuffled
