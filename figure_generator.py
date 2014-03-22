"""
This is a script that takes the functions from figure_maker and creates image files.

"""

from __future__ import division
import os

from figure_maker import *

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

	# Fig 5: Observed RMS error, JHK

	# Fig 6: Distribution of Stetson indices

	# Fig 7: Comparison of periods

	# Fig 8: Median J-H, H-K colors by Megeath class

	# Fig 9: Histogram of stetson indices by class

	# Fig 10: Histograms of K, H-K variability amplitudes

	# Fig 11: Color-color distribution of all Q=2 periodic stars

	# Fig 12: Distribution of periods by class

	# Fig 13, 14, 15: lightcurves

	# Fig 16: Illustration of two example KHK tracks

	# Fig 17: Colorslope threepanel

	# Fig 18: Temporal color experiemnt

	# Fig 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32: Light curves

	# Fig 33: Eclipsing binary light curves

	# 
	return

def generate_figures_test():

	generate_figures_somewhere(test_figure_directory)

def generate_figures_real():

	generate_figures_somewhere(publication_figures)



