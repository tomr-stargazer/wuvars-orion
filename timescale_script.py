"""
This is a script that analyzes color slope timescales.

It calls functions from color_slope_temporal_experiment.

"""

from __future__ import division
import os.path

import atpy

from color_slope_temporal_experiment import *

import matplotlib.pyplot as plt

delta_t_list = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 1000]
#delta_t_list = [10, 40]

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

	fig1 = plt.figure(figsize=(4,5))

	plt.text(20, 56, "Non-shuffled", fontsize=16)

	for non_shuffle in list_of_non_shuffled:

		plt.plot(non_shuffle['time_baseline'], non_shuffle['n_positive_slope'], 'r.')
		plt.plot(non_shuffle['time_baseline'], non_shuffle['n_negative_slope'], 'bx', mew=2)

	plt.xlim(0,200)

	plt.xlabel("Days")
	plt.ylabel("Number of color variables")

	# Lines showing relative fraction
	plt.plot([0,200], [54,54], "r--", lw=0.5, scalex=False, scaley=False)
	plt.plot([0,200], [54/2.,54/2.], "r:", lw=0.5, scalex=False, scaley=False)
	plt.plot([0,200], [36,36], "b--", lw=0.5, scalex=False, scaley=False)
	plt.plot([0,200], [36/2.,36/2.], "b:", lw=0.5, scalex=False, scaley=False)

	plt.text(175, 36.+0.5, "100%", fontsize=10, color='b')
	plt.text(180, 36/2.+0.5, "50%", fontsize=10, color='b')
	plt.text(175, 54.+0.5, "100%", fontsize=10, color='r')
	plt.text(180, 54/2.+0.5, "50%", fontsize=10, color='r')

	fig2 = plt.figure(figsize=(4,5))
	plt.text(20, 56, "Time shuffled", fontsize=16)
	plt.xlabel("Days")
	plt.ylabel("Number of color variables")


	for shuffle in list_of_shuffle_dudes:

		plt.plot(shuffle['time_baseline'], shuffle['n_positive_slope'], 'r.')
		plt.plot(shuffle['time_baseline'], shuffle['n_negative_slope'], 'bx', mew=2)

	plt.xlim(0,200)

	# Lines showing relative fraction
	plt.plot([0,200], [54,54], "r--", lw=0.5, scalex=False, scaley=False)
	plt.plot([0,200], [54/2.,54/2.], "r:", lw=0.5, scalex=False, scaley=False)
	plt.plot([0,200], [36,36], "b--", lw=0.5, scalex=False, scaley=False)
	plt.plot([0,200], [36/2.,36/2.], "b:", lw=0.5, scalex=False, scaley=False)

	# plt.text(175, 36.+0.5, "100%", fontsize=10, color='b')
	plt.text(180, 36/2.+0.5, "50%", fontsize=10, color='b')
	# plt.text(175, 54.+0.5, "100%", fontsize=10, color='r')
	plt.text(180, 54/2.+0.5, "50%", fontsize=10, color='r')


	fig3 = plt.figure(figsize=(4,5))
	plt.text(100, 250, "Non-shuffled", fontsize=16)

	plt.ylabel("Number of variables detected")
	plt.xlabel("Days")

	for non_shuffle in list_of_non_shuffled:

		plt.plot(non_shuffle['time_baseline'], non_shuffle['n_variables'], 'k.')

	plt.xlim(0,200)
	plt.ylim(0,900)

	# lines showing relative fraction
	plt.plot([0,200], [857,857], "k--", lw=0.5, scalex=False, scaley=False)
	plt.text(175, 857+7, "100%", fontsize=10)
	plt.plot([0,200], [857/2,857/2], "k:", lw=0.5, scalex=False, scaley=False)
	plt.text(180, 857/2+7, "50%", fontsize=10)


	fig4 = plt.figure(figsize=(4,5))
	plt.text(100, 250, "Time shuffled", fontsize=16)	
	plt.ylabel("Number of variables detected")	
	plt.xlabel("Days")

	for shuffle in list_of_shuffle_dudes:

		plt.plot(shuffle['time_baseline'], shuffle['n_variables'], 'k.')

	plt.xlim(0,200)
	plt.ylim(0,900)

	# lines showing relative fraction
	plt.plot([0,200], [857,857], "k--", lw=0.5, scalex=False, scaley=False)
	plt.text(175, 857+7, "100%", fontsize=10)
	plt.plot([0,200], [857/2,857/2], "k:", lw=0.5, scalex=False, scaley=False)
	plt.text(180, 857/2+7, "50%", fontsize=10)


	fig5 = plt.figure(figsize=(4,5))
	plt.text(10, 0.23, "Non-shuffled", fontsize=16)		
	plt.ylabel("K amplitude")	
	plt.xlabel("Days")

	for non_shuffle in list_of_non_shuffled:

		plt.errorbar(non_shuffle['time_baseline'], non_shuffle['median_k_amplitude'], yerr=non_shuffle['median_k_deviation'],fmt='k.')

	plt.xlim(0,200)
	plt.ylim(0,0.25)


	fig6 = plt.figure(figsize=(4,5))
	plt.text(10, 0.23, "Time shuffled", fontsize=16)		
	plt.ylabel("K amplitude")
	plt.xlabel("Days")

	for shuffle in list_of_shuffle_dudes:

		plt.errorbar(shuffle['time_baseline'], shuffle['median_k_amplitude'], yerr=shuffle['median_k_deviation'],fmt='k.')

	plt.xlim(0,200)

	return fig1, fig2, fig3, fig4, fig5, fig6


def do_it(**kwargs):
	list_of_shuffle_dudes, non_shuffled = make_shuffle_dudes(**kwargs)
	return plot_shuffle_dudes(list_of_shuffle_dudes, non_shuffled), list_of_shuffle_dudes, non_shuffled

def load_shuffle_dudes_from_october():
	""" 
	On October 21, I created a shuffle run which I hope to be my final run. 
	This function loads the output of that run so it can be re-used. 

	"""

	path = '/Users/tsrice/Documents/Code/wuvars-orion/timescales/21oct2014/'

	list_of_shuffles = []
	for i in range(5):
		list_of_shuffles.append(atpy.Table(path+"shuffle_{0}.fits".format(i)))

	list_of_non_shuffles = []
	for i in range(5):
		list_of_non_shuffles.append(atpy.Table(path+"non_shuffle_{0}.fits".format(i)))

	return list_of_shuffles, list_of_non_shuffles

def plot_saved_runs():
	list_of_shuffle_dudes, non_shuffled = load_shuffle_dudes_from_october()

	return plot_shuffle_dudes(list_of_shuffle_dudes, non_shuffled), list_of_shuffle_dudes, non_shuffled

def save_plots():

	figure_path = os.path.expanduser("~/Dropbox/Bo_Tom/paper/publication_figures/")

# new_nvars.pdf
# new_nvars_shuffled.pdf
# new_kamptime.pdf                 new_redblue.pdf
# new_kamptime_shuffled.pdf        new_redblue_shuffle.pdf

	plots, shuffles, nonshuffles = plot_saved_runs()

	plots[0].savefig(figure_path+"new_redblue.pdf", bbox_inches='tight')
	plots[1].savefig(figure_path+"new_redblue_shuffle.pdf", bbox_inches='tight')
	plots[2].savefig(figure_path+"new_nvars.pdf", bbox_inches='tight')
	plots[3].savefig(figure_path+"new_nvars_shuffled.pdf", bbox_inches='tight')
	plots[4].savefig(figure_path+"new_kamptime.pdf", bbox_inches='tight')
	plots[5].savefig(figure_path+"new_kamptime_shuffled.pdf", bbox_inches='tight')

	return
