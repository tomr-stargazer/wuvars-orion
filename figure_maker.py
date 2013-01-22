"""

This is a script for generating figures for the Orion WFCAM time-series paper.

Each figure (or, sometimes, group of closely related figures) is generated
by its own function, so that you don't HAVE to regenerate them all at the same
time if you only want one.

Guide to variable names:

 =====PERIODICS======
 Currently, we're using 
 `conf_subj_periodics` for subjective periodics,
 `autovars_true_periodics` for the superset of automatically detected and pristine/strict periodic variables, and `autovars_true_periods` when we need their `best_period`s (but NEVER otherwise, for strange reasons)
 `autovars_strict_periodics` for pristine/strict variables, and `autovars_strict_periods` when we need their `best_period`s (but NEVER otherwise, for strange reasons)
 =====NON-PERIODICS======
 `conf_subj_nonpers` for subjective nonperiodics
 `autovars_true_nonpers` for the superset of automatically detected and pristine/strict nonperiodic variables
 `autovars_strict_nonpers` for pristine/strict nonperiodic variables

 =====GLOBAL======
 `autovars_true` for all automatically detected variables (incl. pristines)
 `autovars_strict` for all pristine variables
 `maxvars`


"""

import matplotlib.pyplot as plt

from official_star_counter import *
from color_slope_filtering import (jhk_empty, jhk_filled, jh_empty, jh_filled,
                                   hk_empty, hk_filled)

from montage_script import conf_subj_periodics, conf_subj_nonpers
from plot2 import plot_trajectory_vanilla

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

def f_map_nonpers():
    """
    A figure showing positions of non-periodic variables.

    At some point I'll think more carefully about which maps I actually need
    to produce, and whether APLpy is necessary for all of them.

    """
    
    fig = plt.figure()

    # First group
    plt.plot( np.degrees(conf_subj_nonpers.RA),
              np.degrees(conf_subj_nonpers.DEC), 'wo', 
              label=r"Non-periodics that needed subjective confirmation",
              figure=fig)
    
    # Second group
    plt.plot( np.degrees(autovars_true_nonpers.RA),
              np.degrees(autovars_true_nonpers.DEC), 'bo',
              label=r"Non-periodics with $\geq$ 1 pristine band",
              figure=fig)

    # Third group
    plt.plot( np.degrees(autovars_strict_nonpers.RA),
              np.degrees(autovars_strict_nonpers.DEC), 'ro',
              label="Non-periodics in strictest sample: 3 pristine bands",
              figure=fig)

    # Right ascension is plotted increasing right-to-left, conventionally
    plt.gca().invert_xaxis()

    plt.legend()

    plt.show()

def f_cc_generic(spread, title=""):
    """
    Given an input dataset, makes a color-color plot with cool 
    colors and stuff.

    Parameters
    ----------
    spread : atpy.Table
        A spreadsheet with information on stars whose median 
        J-H and H-K colors want to be plotted.
    title : str
        Desired title for the plot, if any.

    Returns
    -------
    fig : Figure object
        Figure that we plotted onto.
    
    """
    fig = plt.figure()
    ax = plt.gca()

    plot_trajectory_vanilla(ax)

    # First group: only group! Because of how the data quality works.
    plt.scatter(spread.hmk_median, spread.jmh_median, c=spread.k_median,
                vmin=11, vmax=15)

    plt.xlabel(r"median $H-K$")
    plt.ylabel(r"median $J-H$")

    plt.xlim(-0.1,2.5)
    plt.ylim(-0.2, 2.8)
    
    cbar = plt.colorbar()
    cbar.ax.invert_yaxis()
    cbar.set_label(r"Median $K$ magnitude")
    
    if title:
        plt.title(title)

    plt.show()

    return fig

def f_cc_periodics(title=False):
    """
    A figure showing periodic variables' mean color-color space locations.

    Underplotted is the main sequence, reddening lines, and the CTTS locus.
    """

    if title:
        title_string = "Color-color diagram of periodic variables"
    else:
        title_string = ""

    return f_cc_generic(autovars_strict_periodics, title=title_string)

def f_cc_nonpers(title=False):
    """
    A figure showing non-periodic variables' mean color-color space locations.

    Underplotted is the main sequence, reddening lines, and the CTTS locus.
    """

    if title:
        title_string = "Color-color diagram of non-periodic variables"
    else:
        title_string = ""

    return f_cc_generic(autovars_strict_nonpers, title=title_string)

# HERE IS SOME FILTERING FOR COLOR SLOPES... moved to color_slope_filtering.py

def f_cc_color_vars(title=False):
    """
    Shows mean color-color space locations of color-variables.

    Underplotted is the main sequence, reddening lines, and the CTTS locus.
    """
    if title:
        title_string = "Color-color diagram of all high color-change variables"
    else:
        title_string = ""

    return f_cc_generic(jhk_empty, title=title_string)

def f_cc_color_positive(title=False):
    """
    Shows mean color-color space locations of positively-sloped color-variables.

    Underplotted is the main sequence, reddening lines, and the CTTS locus.
    """
    if title:
        title_string = "Color-color diagram: positively (K vs H-K) sloped color-change variables"
    else:
        title_string = ""

    positives = jhk_empty.where( jhk_empty.khk_slope > 0 )

    return f_cc_generic(positives, title=title_string)

def f_cc_color_negative(title=False):
    """
    Shows mean color-color space locations of negatively-sloped color-variables.

    Underplotted is the main sequence, reddening lines, and the CTTS locus.
    """
    if title:
        title_string = "Color-color diagram: negatively (K vs H-K) sloped color-change variables"
    else:
        title_string = ""

    negatives = jhk_empty.where( jhk_empty.khk_slope < 0 )

    return f_cc_generic(negatives, title=title_string)

def f_colorslope_threepanel(title=False):
    """
    Creates a three-panel figure analyzing color slopes just like CHS fig.20.

    A lot of careful filtering takes place in color_slope_filtering.py.
    """

    fig = plt.figure()
    
    s1 = plt.subplot(3,1,1)
    s2 = plt.subplot(3,1,2, sharex=s1, sharey=s1)
    s3 = plt.subplot(3,1,3, sharex=s1, sharey=s1)

    # JHK
    s1.hist(np.degrees(np.arctan(jhk_empty.jhk_slope)), range=[-90, 90],
            bins=36, color='k', histtype='step')
    s1.hist(np.degrees(np.arctan(jhk_filled.jhk_slope)), range=[-90, 90],
            bins=36, color='g')
    s1.set_xlim(-90,90)
    s1.set_xticks([-90, -45, 0, 45, 90])
    s1.set_xticks(np.arange(-90, 90, 15), minor=True)

    # JJH
    s2.hist(np.degrees(np.arctan(jh_empty.jjh_slope)), range=[-90, 90],
            bins=36, color='k', histtype='step')
    s2.hist(np.degrees(np.arctan(jh_filled.jjh_slope)), range=[-90, 90],
            bins=36, color='b')
    s2.set_xlim(-90,90)
    s2.set_xticks([-90, -45, 0, 45, 90])
    s2.set_xticks(np.arange(-90, 90, 15), minor=True)

    # KHK
    s3.hist(np.degrees(np.arctan(hk_empty.khk_slope)), range=[-90, 90],
            bins=36, color='k', histtype='step')
    s3.hist(np.degrees(np.arctan(hk_filled.khk_slope)), range=[-90, 90],
            bins=36, color='r')
    s3.set_xlim(-90,90)
    s3.set_xticks([-90, -45, 0, 45, 90])
    s3.set_xticks(np.arange(-90, 90, 15), minor=True)

    # Labelling stuff

    s3.set_xlabel("Slope (degrees)")
    s3.set_ylabel("N_stars")

    s1.text(-80, 28, r"$J-H$ vs. $H-K$")
    s2.text(-80, 28, r"$J$  vs. $J-H$")
    s3.text(-80, 28, r"$K$  vs. $H-K$")
    
    if title:
        s1.set_title("Histograms of slopes in color-color and color-magnitude space")
    
    plt.show()

f_list = [f_hist_periods, 
          f_map_periods,
          f_map_nonpers,
          f_cc_periodics,
          f_cc_nonpers,
          f_cc_color_vars,
          f_cc_color_positive,
          f_cc_color_negative,
          f_colorslope_threepanel]

def f_allfigures():
    """
    Generates all desired figures.
    """
    for f in f_list:
        f()

    print "generated all figures"
    return
