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
from tablemate_comparisons import (mated_ukvar, ukvar_spread, 
                                   ukvar_periods, source_period_digger)
from tablemate_script import (Megeath2012, Megeath_P, Megeath_D)

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


# Attaching periods to ukvar_spread

def f_cc_and_map_by_megeath_class(sample='all'):
    """
    A color-color diagram where stars are colored by Megeath class.
    
    """

    # Nonperiodic stars only
    if 'non' in sample.lower():
        sample_boolean_criterion = np.isnan(ukvar_periods)
        sample_name = "Non-periodic"
    elif 'per' in sample.lower():
        sample_boolean_criterion = ~np.isnan(ukvar_periods)
        sample_name = "Periodic"
    else:
        sample_boolean_criterion = (np.zeros_like(ukvar_periods) == 0) #all true
        sample_name = "All"

    # Now we want the rows in ukvar_spread that correspond to certain
    # Megeath subsamples.

    disk_indices = (
        # it's got a Megeath2012 counterpart
        (mated_ukvar.Megeath2012_ID != -1) & 
        # whose Class is 'D'
        (Megeath2012.data.Class[mated_ukvar.Megeath2012_index] == 'D') &
        # and it matches our 'periodic/nonperiodic/all' cut.
         sample_boolean_criterion)

    protostar_indices = (
        # it's got a Megeath2012 counterpart
        (mated_ukvar.Megeath2012_ID != -1) & 
        # whose Class is 'P', 'FP', or 'RP'
        ((Megeath2012.data.Class[mated_ukvar.Megeath2012_index] == 'P') |
         (Megeath2012.data.Class[mated_ukvar.Megeath2012_index] == 'FP') |
         (Megeath2012.data.Class[mated_ukvar.Megeath2012_index] == 'RP')) &
        # and it matches our 'periodic/nonperiodic/all' cut.
         sample_boolean_criterion)

    nonmegeath_indices = (
        # it doesn't have a Megeath2012 counterpart
        (mated_ukvar.Megeath2012_ID == -1) & 
        # and it matches our 'periodic/nonperiodic/all' cut.
        sample_boolean_criterion)
    
        
    fig = plt.figure()
    ax = plt.gca()

    plot_trajectory_vanilla(ax)

    plt.plot(ukvar_spread.hmk_median[nonmegeath_indices], 
             ukvar_spread.jmh_median[nonmegeath_indices], 
             'bo', ms=4, label="No Megeath Match")
    plt.plot(ukvar_spread.hmk_median[disk_indices], 
             ukvar_spread.jmh_median[disk_indices], 
             'ro', ms=4, label="Megeath Disks")
    plt.plot(ukvar_spread.hmk_median[protostar_indices], 
             ukvar_spread.jmh_median[protostar_indices], 
             'c*', ms=10, label="Megeath Protostars")

    plt.xlabel(r"median $H-K$")
    plt.ylabel(r"median $J-H$")

    plt.xlim(-0.1,2.5)
    plt.ylim(-0.2, 2.8)
    
    plt.title(sample_name + " variables, colored by Megeath 2012 class")

    plt.legend(loc='lower right')
    
    plt.show()

    fig2 = plt.figure()

    plt.plot(np.degrees(ukvar_spread.RA)[nonmegeath_indices], 
             np.degrees(ukvar_spread.DEC)[nonmegeath_indices], 
             'bo', ms=4, label="No Megeath Match")
    plt.plot(np.degrees(ukvar_spread.RA)[disk_indices], 
             np.degrees(ukvar_spread.DEC)[disk_indices], 
             'ro', ms=4, label="Megeath Disks")
    plt.plot(np.degrees(ukvar_spread.RA)[protostar_indices], 
             np.degrees(ukvar_spread.DEC)[protostar_indices], 
             'c*', ms=10, label="Megeath Protostars")

    plt.legend()
    plt.gca().invert_xaxis()

    plt.show()

    return (fig, fig2)


    

def f_periods_by_megeath_class(title=False):
    """
    A histogram of periods for stars that have Megeath classes.

    """ 
    # we're using: mated_ukvar AND ukvar_periods.
    # We'll also have to import Megeath2012 from tablemate_script.

    # Okay, so we want to do something sensitive:
    # figure out the intersection between UKvar stars that have PERIODS
    # and Ukvar stars that are mated to Megeath2012 sources.

    # These are the indices (in the UKvar system) of such overlapped stars.
    periodic_megeath_stars_indices = (mated_ukvar.Megeath2012_ID != -1) & (~np.isnan(ukvar_periods))

    # This is an array of their Spitzer Classes. 
    periodic_megeath_stars_megeath_class = Megeath2012.data.Class[mated_ukvar.Megeath2012_index[periodic_megeath_stars_indices]]

    # This is an array of their periods. I hope.
    periodic_megeath_stars_period = ukvar_periods[periodic_megeath_stars_indices]

    # These are the periodic stars without Megeath correspondence.
    periodic_nonmegeath_stars_indices = ~periodic_megeath_stars_indices
    # and their periods
    periodic_nonmegeath_stars_period = ukvar_periods[periodic_nonmegeath_stars_indices]


    fig = plt.figure()

    sub1 = plt.subplot(3,1,1)
    plt.hist(periodic_megeath_stars_period[periodic_megeath_stars_megeath_class == 'P'], range=[0,20], bins=30, color='c')

    sub2 = plt.subplot(3,1,2, sharex=sub1)
    plt.hist(periodic_megeath_stars_period[periodic_megeath_stars_megeath_class == 'D'], range=[0,20], bins=30, color='r')

    sub3 = plt.subplot(3,1,3, sharex=sub1)
    plt.hist(periodic_nonmegeath_stars_period, range=[0,20], bins=30, 
             color='b')
    
    sub3.set_xlabel("Period (days)")

    sub1.text(10, 1, "Megeath Periodic Protostar sample")
    sub2.text(10,20, "Megeath Periodic Disk sample")
    sub3.text(10,30, "Periodic UKvars that did not \ncorrespond to Megeath objects")

    sub1.set_title("Periodic UKvar stars, with class from Megeath 2012")

    plt.show()

    return fig

def f_period_lit_comparisons():
    """
    A figure plotting the periods that we derive in our study
    against literature periods.
    """
    lit_periods = source_period_digger(mated_ukvar)

    # what we REALLY need is a table that does ONCvars and best periods...
    # problem solved! `ukvar_periods`
    
    fig = plt.figure()


    plt.plot([0,40],[0,40], 'b--')
    plt.plot([0,40],[0,80], 'g:')
    plt.plot([0,80],[0,40], 'g:')
    
    # 
    plt.plot(ukvar_periods, lit_periods.GCVS_period, 'o', 
             label='GCVS periods')
    plt.plot(ukvar_periods, lit_periods.CHS01_period, 'o', 
             label='CHS01 periods')
    plt.plot(ukvar_periods, lit_periods.YSOVAR_period, 'o', 
             label='YSOVAR periods')
    plt.plot(ukvar_periods, lit_periods.Herbst2002_period, 'o', 
             label='Herbst2002 periods')
    plt.plot(ukvar_periods, lit_periods.Parihar2009_period, 'o', 
             label='Parihar2009 periods')
    plt.plot(ukvar_periods, lit_periods.RodriguezLedesma2009_period, 'o', 
             label='RodriguezLedesma2009 periods')

    
    plt.legend()

    plt.xlabel("Periods derived in our study (days)")
    plt.ylabel("Literature periods (days)")

    plt.gca().set_aspect('equal')

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
