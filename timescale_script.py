"""
This is a script that analyzes color slope timescales.

It calls functions from color_slope_temporal_experiment.

"""

from color_slope_temporal_experiment import *

import matplotlib.pyplot as plt

#delta_t_list = [5,10,20, 25, 30, 40, 50, 75, 100]
delta_t_list = [10, 40]

def make_shuffle_dudes(n_iterations=3):

	list_of_non_shuffled = []

	for i in range(n_iterations):
		list_of_non_shuffled.append(
			calculate_color_slope_ratios_versus_time_baseline(
				delta_t_list=delta_t_list, date_offset=i*30, shuffle_dates=False) )

	list_of_shuffle_dudes = []	

	for i in range(n_iterations):
		list_of_shuffle_dudes.append(
			calculate_color_slope_ratios_versus_time_baseline(
				delta_t_list=delta_t_list, shuffle_dates=True) )

	return list_of_shuffle_dudes, list_of_non_shuffled

def plot_shuffle_dudes(list_of_shuffle_dudes, list_of_non_shuffled):

	fig1 = plt.figure()

	plt.title("Non shuffled. Each run offset by 30 days.")

	for non_shuffle in list_of_non_shuffled:

		plt.plot(non_shuffle.time_baseline, non_shuffle.n_positive_slope, 'r.')
		plt.plot(non_shuffle.time_baseline, non_shuffle.n_negative_slope, 'b.')

	fig2 = plt.figure()

	for shuffle in list_of_shuffle_dudes:

		plt.plot(shuffle.time_baseline, shuffle.n_positive_slope, 'r.')
		plt.plot(shuffle.time_baseline, shuffle.n_negative_slope, 'b.')

	return fig1, fig2


def do_it():
	list_of_shuffle_dudes, non_shuffled = make_shuffle_dudes()
	return plot_shuffle_dudes(list_of_shuffle_dudes, non_shuffled), list_of_shuffle_dudes, non_shuffled
