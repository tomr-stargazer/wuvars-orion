"""
This is a script whose purpose is to identify long periodic candidates 
and let me study them.

"""

from __future__ import division
import os

import numpy as np
import matplotlib.pyplot as plt

from orion_plot import OrionStarData
from tablemate_comparisons import ukvar_spread
from official_star_counter import maxvars_spread_per
from variables_data_filterer import variables_photometry
from lightcurve_maker import lc_and_phase_and_colors
from table_maker import make_megeath_class_column


# These can be broken into two groups:
# 1. Anyone with a period longer than 20 days from the official periodics (shorter than 20 days)
# 2. Long periods identified by hand greater than 50 days.

def long_periodic_selector( spread, min_period=50, max_period=200 ):
    """
    Selects real periodic variables using periodogram parameters.

    Currently only uses Lomb-Scargle input data. Soon to be fixed.

    Parameters
    ----------
    spread : atpy.Table
        Table of spreadsheet info on variable stars.

    Returns
    -------
    periodic_spread : atpy.Table
        Subset of `spread` with only "real" periodics.
    
    """

    s = spread

    r = s.where(
        ( # J, H
            (s.j_lsp_per < s.h_lsp_per * 1.05) &
            (s.j_lsp_per > s.h_lsp_per * 0.95) &
            (s.j_lsp_per > min_period) & (s.j_lsp_per < max_period) &
            (s.j_lsp_pow > 12) & (s.h_lsp_pow > 12) 
            ) |
        ( # H, K
            (s.h_lsp_per < s.k_lsp_per * 1.05) &
            (s.h_lsp_per > s.k_lsp_per * 0.95) &
            (s.h_lsp_per > min_period) & (s.h_lsp_per < max_period) &
            (s.h_lsp_pow > 12) & (s.k_lsp_pow > 12) 
            ) |
        ( # J, K
            (s.j_lsp_per < s.k_lsp_per * 1.05) &
            (s.j_lsp_per > s.k_lsp_per * 0.95) &
            (s.j_lsp_per > min_period) & (s.j_lsp_per < max_period) &
            (s.j_lsp_pow > 12) & (s.k_lsp_pow > 12) 
            ) |
        ( #J
            (s.j_lsp_pow > 15) & (s.j_lsp_per > min_period) & (s.j_lsp_per < max_period) 
            ) |
        ( #H
            (s.h_lsp_pow > 15) & (s.h_lsp_per > min_period) & (s.h_lsp_per < max_period) 
            ) |
        ( #K
            (s.k_lsp_pow > 15) & (s.k_lsp_per > min_period) & (s.k_lsp_per < max_period) 
            ) 
        )
    
    periodic_spread = r
    return periodic_spread


def best_long_period( periodic_spread, min_period=50, max_period=200 ):
    """ 
    A function that chooses the best period of the six returned.

    Currently operates only on LSP input, just like periodic_selector.

    Parameters
    ----------
    periodic_spread : atpy.Table
        Table containing periodic variables

    Returns
    -------
    periodic_spread_updated : atpy.Table
        Input table with new "best_period" column added.

    """

    best_period = -1.*np.ones_like( periodic_spread.j_lsp_per )

    r = periodic_spread

    for i in range(len(periodic_spread)):
        # J, H
        if ((r.j_lsp_per[i] < r.h_lsp_per[i] * 1.05) and
            (r.j_lsp_per[i] > r.h_lsp_per[i] * 0.95) and
            (r.j_lsp_per[i] > min_period) and (r.j_lsp_per[i] < max_period) and
            (r.j_lsp_pow[i] > 12) and (r.h_lsp_pow[i] > 12)
            ):
            best_period[i] = r.h_lsp_per[i]
        # H, K
        elif ((r.h_lsp_per[i] < r.k_lsp_per[i] * 1.05) and
              (r.h_lsp_per[i] > r.k_lsp_per[i] * 0.95) and
              (r.h_lsp_per[i] > min_period) and (r.h_lsp_per[i] < max_period) and
              (r.h_lsp_pow[i] > 12) and (r.k_lsp_pow[i] > 12)
              ):
            best_period[i] = r.h_lsp_per[i]
        # J, K
        elif ((r.j_lsp_per[i] < r.k_lsp_per[i] * 1.05) and
              (r.j_lsp_per[i] > r.k_lsp_per[i] * 0.95) and
              (r.j_lsp_per[i] > min_period) and (r.j_lsp_per[i] < max_period) and
              (r.j_lsp_pow[i] > 12) and (r.k_lsp_pow[i] > 12)
              ):
            best_period[i] = r.k_lsp_per[i]
        # J
        elif (r.j_lsp_pow[i] > 15) and (r.j_lsp_per[i] > min_period) and (r.j_lsp_per[i] < max_period):
            best_period[i] = r.j_lsp_per[i]
        # H
        elif (r.h_lsp_pow[i] > 15) and (r.h_lsp_per[i] > min_period) and (r.h_lsp_per[i] < max_period):
            best_period[i] = r.h_lsp_per[i]
        # K
        elif (r.k_lsp_pow[i] > 15) and (r.k_lsp_per[i] > min_period) and (r.k_lsp_per[i] < max_period):
            best_period[i] = r.k_lsp_per[i]
        else:
            print "SOMETHING IS FISHY HERE"

    r.add_column("best_period", best_period)

    periodic_spread_updated = r
    return periodic_spread_updated


megeath_class_column = make_megeath_class_column()

path = os.path.expanduser("~/Dropbox/Bo_Tom/lightcurve_book/long_periods/")
path2 = os.path.expanduser("~/Dropbox/Bo_Tom/lightcurve_book/short_periods/")

def find_20_50_day_periodics_and_save_to_file():
	blp = best_long_period(long_periodic_selector(maxvars_spread_per, max_period=100), max_period=100)
	ukvar_blp = blp.where(np.in1d(blp.SOURCEID, ukvar_spread.SOURCEID))

	print "There are {0} stars with nominal periods between 50 and 100.".format(len(ukvar_blp))

	for sid, period in zip(ukvar_blp.SOURCEID, ukvar_blp.best_period):
	    sd = OrionStarData(variables_photometry, sid, ukvar_spread.UKvar_ID[ukvar_spread.SOURCEID==sid][0])
	    fig = lc_and_phase_and_colors(sd, period)
	    fig.ax_j_phase.set_title("ONCvar {}".format(sd.name))
	    fig.ax_j_lc.set_title(sid)
	    fig.savefig("{0}/{1}/{2}.png".format(path, "50_100", sd.name))
	    plt.close()

	blp2 = best_long_period(long_periodic_selector(maxvars_spread_per, min_period=20, max_period=50), min_period=20, max_period=50)
	ukvar_blp2 = blp2.where(np.in1d(blp2.SOURCEID, ukvar_spread.SOURCEID))

	print "There are {0} stars with nominal periods between 20 and 50.".format(len(ukvar_blp2))

	for sid, period in zip(ukvar_blp2.SOURCEID, ukvar_blp2.best_period):
	    sd = OrionStarData(variables_photometry, sid, ukvar_spread.UKvar_ID[ukvar_spread.SOURCEID==sid][0])
	    fig = lc_and_phase_and_colors(sd, period)
	    fig.ax_j_phase.set_title("ONCvar {}".format(sd.name))
	    fig.ax_j_lc.set_title(sid)
	    fig.savefig("{0}/{1}/{2}.png".format(path, "20_50", sd.name))
	    plt.close()

	blp3 = best_long_period(long_periodic_selector(maxvars_spread_per, min_period=10, max_period=20), min_period=10, max_period=20)
	ukvar_blp3 = blp3.where(np.in1d(blp3.SOURCEID, ukvar_spread.SOURCEID))

	print "There are {0} stars with nominal periods between 10 and 20.".format(len(ukvar_blp3))

	for sid, period in zip(ukvar_blp3.SOURCEID, ukvar_blp3.best_period):
	    sd = OrionStarData(variables_photometry, sid, ukvar_spread.UKvar_ID[ukvar_spread.SOURCEID==sid][0])
	    fig = lc_and_phase_and_colors(sd, period)
	    fig.ax_j_phase.set_title("ONCvar {}".format(sd.name))
	    fig.ax_j_lc.set_title(sid)
	    fig.savefig("{0}/{1}/{2}.png".format(path, "10_20", sd.name))
	    plt.close()

def find_min_max_day_periodics_and_write(min_period=2, max_period=10, path=path2):
	blp = best_long_period(long_periodic_selector(maxvars_spread_per, min_period=min_period, max_period=max_period),
	                       min_period=min_period, max_period=max_period)
	ukvar_blp = blp.where(np.in1d(blp.SOURCEID, ukvar_spread.SOURCEID))

	print "There are {0} stars with nominal periods between {1} and {2}.".format(len(ukvar_blp), min_period, max_period)

	for sid, period in zip(ukvar_blp.SOURCEID, ukvar_blp.best_period):
	    sd = OrionStarData(variables_photometry, sid, ukvar_spread.UKvar_ID[ukvar_spread.SOURCEID==sid][0])
	    fig = lc_and_phase_and_colors(sd, period)
	    fig.ax_j_phase.set_title("ONCvar {} ({})".format(sd.name, megeath_class_column[ukvar_spread.SOURCEID==sid][0]))
	    fig.ax_j_lc.set_title("{0}, Q={1}".format(sid, int((ukvar_spread.autovar+ukvar_spread.strict)[[ukvar_spread.SOURCEID==sid]][0])))
	    fig.savefig("{0}/{1}_{2}/{3}.png".format(path, min_period, max_period, sd.name))
	    plt.close()

