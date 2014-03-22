"""
This is a script that takes the functions from figure_maker and creates image files.

"""

from __future__ import division
import os

from figure_maker import *
from swolk_experiment import match_spitzer_to_ukirt

publication_figures = os.path.expanduser("~/Dropbox/Bo_Tom/paper/publication_figures/")
publication_lcs = os.path.expanduser("~/Dropbox/Bo_Tom/paper/publication_lcs/")

test_figure_directory = os.path.expanduser("~/Dropbox/Bo_Tom/paper/test_figure_directory/")

def generate_figures_somewhere(path):

	# Fig 1: history of IR monitoring campaigns
	fig1 = f_comparison_observing_log()
	fig1.savefig(path+"comparison_observing_log.pdf")

	# Fig 2: Tiles
	fig2 = f_observing_map()
	fig2.savefig(path+"observing_log_map.pdf")

	# Fig 3: APLpy map of 1202 variables
	"""
	not ready yet
	fig3.savefig(path+"figure_1_prettymap_september10.pdf")
	"""

	# Fig 4: eight example lightcurves
	"""
	not ready yet
	fig4.savefig(path+"example_lcs_draft.png")
	"""

	# Fig 5: Observed RMS error, JHK
	fig5 = f_sensitivity_per_band()
	fig5.savefig(path+"sensitivity_per_band.pdf")

	# Fig 6: Distribution of Stetson indices
	fig6 = f_stetson_versus_Hmag_strict_candidates()
	fig6.savefig(path+"Stetson_vs_Hmag.pdf")

	# Fig 7: Comparison of periods
	f_period_lit_comparisons().savefig(path+"period_lit_comparisons.pdf")

	# Fig 8: Median J-H, H-K colors by Megeath class
	f_cc_cmd_and_map_by_megeath_class()[0].savefig(path+"cc_by_class.pdf")

	# Fig 9: Histogram of stetson indices by class
	match_spitzer_to_ukirt()[3].savefig(path+"Stetson_by_class.pdf")

	# Fig 10: Histograms of K, H-K variability amplitudes
	j, h, k, jmh, hmk = f_magnitude_hists_by_class()
	k.savefig(path+"delta_k_hists.pdf")
	hmk.savefig(path+"delta_hmk_hists.pdf")

	# Fig 11: Color-color distribution of all Q=2 periodic stars
	fig11 = f_cc_periodics()
	plt.text(1.25, 1, "Periodic variables", fontsize=18)
	fig11.savefig(path+"cc_periodics.pdf")

	# Fig 12: Distribution of periods by class
	f_periods_by_megeath_class()[0].savefig(path+"period_distributions.pdf")

	# Fig 13, 14, 15: lightcurves

	# Fig 16: Illustration of two example KHK tracks

	# Fig 17: Colorslope threepanel
	f_colorslope_threepanel().savefig(path+"color_slope_threepanel.pdf")

	# Fig 18: Temporal color experiment

	# Fig 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32: Light curves

	# Fig 33: Eclipsing binary light curves

	# 
	return

def generate_figures_test():

	generate_figures_somewhere(test_figure_directory)

def generate_figures_real():

	generate_figures_somewhere(publication_figures)



