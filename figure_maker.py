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

    plt.hist(autovars_true_periods.best_period, bins=22, range=[2,46], 
             color='b', label=r"Periodics with $\geq$ 1 pristine band",
             figure=fig)

    plt.hist(autovars_strict_periods.best_period, bins=22, range=[2,46], 
             color='r', label="Periodics in strictest sample: 3 pristine bands",
             figure=fig)

    plt.legend()
    
    plt.show()
