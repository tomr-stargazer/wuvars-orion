"""

This is a script for generating figures for the Orion WFCAM time-series paper.

Each figure (or, sometimes, group of closely related figures) is generated
by its own function, so that you don't HAVE to regenerate them all at the same
time if you only want one.

"""

import matplotlib.pyplot as plt

from official_star_counter import *

from montage_script import conf_subj_periodics, conf_subj_nonpers

# As a test, let's make a histogram of periods.

# Guide to variable names:
# Currently, we're using 
# `conf_subj_periodics` for subjective periodics,
# `autovars_true_periodics` for the superset of automatically detected and pristine/strict

# Filled: strict dudes
# Cross-hatched: autovars_true
# open: subjectives

def f_hist_periods():
    """ 
    A figure showing a histogram of periods reported for periodic variables.
    """

    fig = plt.figure()

    # First group
    plt.hist(np.concatenate((conf_subj_periodics.best_period, 
                         autovars_true_periods.best_period)), 
         bins=22, range=[2,46], color='w', 
         label=r"Periodics that needed subjective confirmation", 
             figure=fig)

    # Second group
    plt.hist(autovars_true_periods.best_period, bins=22, range=[2,46], 
             color='b', label=r"Periodics with $\geq$ 1 pristine band",
             figure=fig)

    # Third group
    plt.hist(autovars_strict_periods.best_period, bins=22, range=[2,46], 
             color='r', label="Periodics in strictest sample: 3 pristine bands",
             figure=fig)

    plt.legend()
    
    plt.xlabel("Period (days)")
    plt.ylabel("Number of periodic stars")
    
    plt.show()

    
def f_map_periods():
    """
    A figure showing positions of periodic variables.

    At some point I'll think more carefully about which maps I actually need
    to produce, and whether APLpy is necessary for all of them.

    """

    fig = plt.figure()

    # First group
    plt.plot( np.degrees(conf_subj_periodics.RA),
              np.degrees(conf_subj_periodics.DEC), 'wo', 
              label=r"Periodics that needed subjective confirmation",
              figure=fig)
    
    # Second group
    plt.plot( np.degrees(autovars_true_periodics.RA),
              np.degrees(autovars_true_periodics.DEC), 'bo',
              label=r"Periodics with $\geq$ 1 pristine band",
              figure=fig)

    # Third group
    plt.plot( np.degrees(autovars_strict_periodics.RA),
              np.degrees(autovars_strict_periodics.DEC), 'ro',
              label="Periodics in strictest sample: 3 pristine bands",
              figure=fig)

    # Right ascension is plotted increasing right-to-left, conventionally
    plt.gca().invert_xaxis()

    plt.legend()

    plt.show()


def f_map_variables():
    """
    A figure showing positions of all variables.

    At some point I'll think more carefully about which maps I actually need
    to produce, and whether APLpy is necessary for all of them.

    """
    
    pass
