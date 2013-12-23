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

from __future__ import division

import matplotlib.pyplot as plt
import scipy.stats

from official_star_counter import *
from color_slope_filtering import (jhk_empty, jhk_filled, jh_empty, jh_filled,
                                   hk_empty, hk_filled)
from tablemate_comparisons import (mated_ukvar, ukvar_spread, 
                                   ukvar_periods, source_period_digger)
from tablemate_script import (Megeath2012, Megeath_P, Megeath_D)
from orion_tablemate import index_secondary_by_primary
from variables_data_filterer import filter_by_tile, variables_photometry
from table_maker import make_megeath_class_column

from montage_script import conf_subj_periodics, conf_subj_nonpers
from plot2 import plot_trajectory_vanilla
from helpers3 import band_cut
import robust as rb

# Let's grab IRAC colors from Megeath.
megeath2012_by_ukvar = index_secondary_by_primary(mated_ukvar, Megeath2012)

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
                vmin=11, vmax=15, cmap='cubehelix_r')

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


def f_color_slopes_and_periods(title1="K, H-K color slope distributions: "
                               "Periodic vs Non-Periodic",
                               title2="Color slopes versus periods, "
                               "for periodic stars"):
    """
    Generates two figures relating K, H-K color slopes with periods.
    
    a) two-panel histogram (purple/yellow) of color slopes for periodic 
       vs nonperiodic stars.
    b) Scatter plot of color slope versus period, for stars with 
       well-defined color-slopes and periods.

    """

    selection = np.in1d(ukvar_spread.SOURCEID, hk_filled.SOURCEID)

    color_periodics = ukvar_spread.where(selection & 
                                         (ukvar_spread.periodic > 0))
    color_periods = ukvar_periods[selection & (ukvar_spread.periodic > 0)]

    color_nonperiodics = ukvar_spread.where(selection & 
                                            (ukvar_spread.periodic == 0))

    # Fig 1 is the double histogram.
    fig1 = plt.figure()
    sub1 = plt.subplot(2,1,1)

    sub1.hist(np.degrees(np.arctan(color_periodics.khk_slope)), 
              range=[-90, 90], bins=36, color='m')
    plt.text(-45,4, "K, H-K color slopes for Periodic stars")
    sub1.set_title(title1)

    sub2 = plt.subplot(2,1,2, sharex=sub1)

    sub2.hist(np.degrees(np.arctan(color_nonperiodics.khk_slope)), 
              range=[-90, 90], bins=36, color='y')
    plt.text(-45,4, "K, H-K color slopes for Non-Periodic stars")
    
    sub2.set_xlabel("K, H-K color slope (degrees)")
    sub2.set_xlim(-90,90)
    sub2.set_xticks([-90,-45,0,45,90])

    # Fig 2 is the scatterplot.
    fig2 = plt.figure()

    plt.plot(color_periods, 
              np.degrees(np.arctan(color_periodics.khk_slope)), 'ko')

    plt.xlabel("Period, days")
    plt.ylabel("K, H-K color slope (degrees)")

    plt.ylim(-90, 90)
    plt.yticks([-90, -45, 0, 45, 90])
    plt.gca().set_yticks(np.arange(-90, 90, 15), minor=True)

    plt.text(30,-60, "Disk activity")
    plt.text(30,60, "Dust (A_V)")

    plt.title(title2)

    plt.show()

    return fig1, fig2

    

# Attaching periods to ukvar_spread

def f_cc_cmd_and_map_by_megeath_class(sample='all', title=True):
    """
    A color-color diagram where stars are colored by Megeath class.

    Also a CMD and a map.
    
    """

    megeath_class_column = make_megeath_class_column()

    # Nonperiodic stars only
    if 'non' in sample.lower():
        sample_boolean_criterion = np.isnan(ukvar_periods)
        sample_name = "Non-periodic"
    elif 'per' in sample.lower():
        sample_boolean_criterion = ~np.isnan(ukvar_periods)
        sample_name = "Periodic"
    elif 'strict' in sample.lower():
        sample_boolean_criterion = (ukvar_spread.strict == 1)
        sample_name = "Q=2"
    else:
        sample_boolean_criterion = (np.zeros_like(ukvar_periods) == 0) #all true
        sample_name = "All"

    # Now we want the rows in ukvar_spread that correspond to certain
    # Megeath subsamples.

    disk_indices = (
        # its Class is 'D'
        (megeath_class_column == 'D') &
        # and it matches our 'periodic/nonperiodic/all' cut.
         sample_boolean_criterion)

    protostar_indices = (
        (megeath_class_column == 'P') & sample_boolean_criterion)

    nondisk_indices = (
        (megeath_class_column == 'ND') & sample_boolean_criterion)

    unknown_indices = (
        (megeath_class_column == 'na') & sample_boolean_criterion)
    
        
    fig = plt.figure()
    ax = plt.gca()

    plot_trajectory_vanilla(ax, a_k=3)

    plt.plot(ukvar_spread.hmk_median[nondisk_indices],
             ukvar_spread.jmh_median[nondisk_indices],
             'bo', ms=4, label="Non-disks")
    plt.plot(ukvar_spread.hmk_median[disk_indices],
             ukvar_spread.jmh_median[disk_indices],
             'ro', ms=4, label="Disks")
    plt.plot(ukvar_spread.hmk_median[protostar_indices],
             ukvar_spread.jmh_median[protostar_indices],
             'c*', ms=10, label="Protostars")

    plt.xlabel(r"median $H-K$")
    plt.ylabel(r"median $J-H$")

    plt.xlim(-0.1,3.1)
    plt.ylim(-0.2, 4.4)

    if title:
        plt.title(sample_name + " variables, colored by Megeath+2012 class")

    plt.legend(loc='lower right')


    fig3 = plt.figure()
    ax3 = plt.gca()

    plot_trajectory_vanilla(ax, a_k=3)

    plt.plot(ukvar_spread.hmk_median[nondisk_indices],
             ukvar_spread.k_median[nondisk_indices],
             'bo', ms=4, label="Non-disks")
    plt.plot(ukvar_spread.hmk_median[disk_indices],
             ukvar_spread.k_median[disk_indices],
             'ro', ms=4, label="Disks")
    plt.plot(ukvar_spread.hmk_median[protostar_indices],
             ukvar_spread.k_median[protostar_indices],
             'c*', ms=10, label="Protostars")

    plt.xlabel(r"median $H-K$")
    plt.ylabel(r"median $K$ mag")

    plt.xlim(-0.1,3.1)
    plt.ylim(17, 8)
    
    plt.title(sample_name + " variables, colored by Megeath 2012 class")

    plt.legend(loc='upper right')


    fig2 = plt.figure()

    plt.plot(np.degrees(ukvar_spread.RA)[nondisk_indices], 
             np.degrees(ukvar_spread.DEC)[nondisk_indices], 
             'bo', ms=4, label="Non-disks")
    plt.plot(np.degrees(ukvar_spread.RA)[disk_indices], 
             np.degrees(ukvar_spread.DEC)[disk_indices], 
             'ro', ms=4, label="Disks")
    plt.plot(np.degrees(ukvar_spread.RA)[protostar_indices], 
             np.degrees(ukvar_spread.DEC)[protostar_indices], 
             'c*', ms=10, label="Protostars")

    plt.legend()
    plt.gca().invert_xaxis()

    plt.show()

    return (fig, fig2, fig3)


    

def f_periods_by_megeath_class(title="Periodic UKvar stars, with class from Megeath 2012"):
    """
    A histogram of periods for stars that have Megeath classes.

    Returns
    -------
    fig : plt.figure
    three np.ndarrays 
        These arrays contain the distribution of periods for 
        (a) protostars,
        (b) disked stars, and
        (c) non-disked stars
        (on the basis of Megeath2012 membership/Class). Use these
        for K-S tests if you gotta (see example)

    Example:
    In [15]: foo = f_periods_by_megeath_class()
    In [16]: red = foo[2]
    In [17]: blue = foo[3]
    
    In [18]: scipy.stats.ks_2samp(red, blue)
    Out[18]: (0.32200088003520139, 1.2771000514405625e-22)

    """ 

    megeath_class_column = make_megeath_class_column()

    fig = plt.figure()

    sub1 = plt.subplot(3,1,1)
    plt.hist(ukvar_periods[megeath_class_column == 'P'],
             range=[0,20], bins=40, color='c')

    sub2 = plt.subplot(3,1,2, sharex=sub1)
    plt.hist(ukvar_periods[megeath_class_column == 'D'],
             range=[0,20], bins=40, color='r')

    sub3 = plt.subplot(3,1,3, sharex=sub1)
    plt.hist(ukvar_periods[megeath_class_column == 'ND'],
             range=[0,20], bins=40, color='b')
    
    sub3.set_xlabel("Period (days)")

    sub1.text(10, 1, "Megeath Periodic Protostar sample")
    sub2.text(10,15, "Megeath Periodic Disk sample")
    sub3.text(10,25, "Megeath Periodic Non-disk sample")

    if title:
        sub1.set_title(title)

    plt.show()

    print "scipy.stats.ks_2samp(disks, no_disks):"
    print scipy.stats.ks_2samp(ukvar_periods[megeath_class_column == 'D'],
                               ukvar_periods[megeath_class_column == 'ND'])

    return (fig,
            ukvar_periods[megeath_class_column == 'P'], 
            ukvar_periods[megeath_class_column == 'D'], 
            ukvar_periods[megeath_class_column == 'ND'])

def f_period_lit_comparisons(pretty=True):
    """
    A figure plotting the periods that we derive in our study
    against literature periods.

    Parameters
    ----------
    pretty : bool, optional, default: True
        Make this plot publication-quality? 
        Involves scaling the axes and changing the size of the figure.
        
    """
    lit_periods = source_period_digger(mated_ukvar)

    # what we REALLY need is a table that does UKvars and best periods...
    # problem solved! `ukvar_periods`
    
    fig = plt.figure(figsize=(8,8))


    plt.plot([0,40],[0,40], 'b--')
    plt.plot([0,40],[0,80], 'g:')
    plt.plot([0,80],[0,40], 'g:')
    
    plt.plot(ukvar_periods, lit_periods.GCVS_period, 'o', 
             label='General Catalog of Variable Stars')
    plt.plot(ukvar_periods, lit_periods.CHS01_period, 'o', 
             label='Carpenter+2001')
    plt.plot(ukvar_periods, lit_periods.YSOVAR_period, 'o', 
             label='(YSOVAR) Morales-Calderon+2011')
    plt.plot(ukvar_periods, lit_periods.Herbst2002_period, 'o', 
             label='Herbst+2002')
    plt.plot(ukvar_periods, lit_periods.Parihar2009_period, 'o', 
             label='Parihar+2009')
    plt.plot(ukvar_periods, lit_periods.RodriguezLedesma2009_period, 'o', 
             label='Rodriguez-Ledesma+2009')
    
    plt.legend(numpoints=1, loc='Upper Left', framealpha=0.5)

    plt.xlabel("Periods derived in our study (days)")
    plt.ylabel("Literature periods (days)")

    plt.gca().set_aspect('equal')

    if pretty:
        plt.xlim(0,20)
        plt.ylim(0,20)

    plt.show()


def f_magnitude_hists_by_class(threepanels=True, onepanels=False):
    """
    Makes a series of multipanel histograms of variability.
    Uses "strict" sources only for these.
    
    """

    megeath_class_column = make_megeath_class_column()
    
    strict_protostars = ukvar_spread.where(
        (ukvar_spread.strict == 1) & (megeath_class_column == 'P') )

    strict_disks = ukvar_spread.where(
        (ukvar_spread.strict == 1) & (megeath_class_column == 'D'))

    strict_nondisks = ukvar_spread.where(
        (ukvar_spread.strict == 1) & (megeath_class_column == 'ND'))

    # Let's test the J mag aspect of this, and then define some dicts or forloops to iterate through all "5" bands.

    names = ['J mag', 'H mag', 'K mag', 'J-H color', 'H-K color']
    bands = ['j', 'h', 'k', 'jmh', 'hmk']

    figs = []

    hist_kwargs = {'range':(0,2), 'bins':20}

    if threepanels:
        for b, n in zip(bands, names):

            j_fig = plt.figure()

            jsub1 = plt.subplot(3,1,1)
            jsub1.hist(strict_protostars['%s_ranger' % b], color='c', 
                       **hist_kwargs)
            jsub1.text(0.5, 0.65, "Megeath protostars \n"
                       r"median $\Delta %s: $%.2f \pm %.2f$" % (
                    n.replace(' ', '$ '), 
                    np.median(strict_protostars['%s_ranger' % b]),
                    rb.mad(strict_protostars['%s_ranger' % b])),
                       transform = jsub1.transAxes)

            jsub2 = plt.subplot(3,1,2, sharex=jsub1)
            jsub2.hist(strict_disks['%s_ranger' % b], color='r', **hist_kwargs)
            jsub2.text(0.5, 0.65, "Megeath disks \n"
                       r"median $\Delta %s: $%.2f \pm %.2f$" % (
                    n.replace(' ', '$ '), 
                    np.median(strict_disks['%s_ranger' % b]),
                    rb.mad(strict_disks['%s_ranger' % b])),
                       transform = jsub2.transAxes)

            jsub3 = plt.subplot(3,1,3, sharex=jsub1)
            jsub3.hist(strict_nondisks['%s_ranger' % b], color='b', 
                       **hist_kwargs)
            jsub3.text(0.5, 0.65, "Megeath non-disks \n"
                       r"median $\Delta %s: $%.2f \pm %.2f$" % (
                    n.replace(' ', '$ '), 
                    np.median(strict_nondisks['%s_ranger' % b]),
                    rb.mad(strict_nondisks['%s_ranger' % b])),
                       transform = jsub3.transAxes)

            jsub1.set_title("%s range (robust) for pristine-data variables"%n)
            jsub3.set_xlabel(r"$\Delta %s (outlier-proof)" % 
                             n.replace(' ', '$ '))


    if onepanels:

        fig = plt.figure()
        
        plt.hist(strict_nondisks['k_ranger'], 
                 color='b', hatch='/', label='Megeath Non-disks',
                 **hist_kwargs)
        plt.hist(strict_disks['k_ranger'], 
                 color='r', alpha=0.5, hatch='\\', label='Megeath Disks',
                 **hist_kwargs)
        plt.hist(strict_protostars['k_ranger'], 
                 color='c', hatch='--', label='Megeath Protostars',
                 **hist_kwargs)

        plt.title("K magnitude range (robust) for pristine-data variables")
        plt.xlabel(r"$\Delta K$ magnitude (outlier-proof)")

        plt.legend()

            
    plt.show()


def f_stetson_versus_Hmag_strict_candidates(
        title="Stetson index vs median H magnitude for Q=2 stars",
        yscale='linear'):
    """
    Plots Stetson against median H-mag for strict candidates 
    (i.e., all stars with Q=2.)

    Also makes a cool side-histogram which is arguably the more useful
    part of the figure.

    Can be optionally log-scaled (to show all of the data) or linear scaled
    (to show the zero-through-one region faithfully)

    """

    fig = plt.figure()

    ax_plot = fig.add_axes( (0.1, 0.1, 0.6, 0.8) )
    
    plt.plot(autocan_strict.h_median, autocan_strict.Stetson, 'ro', ms=2)

    # put some lines in there
    plt.plot([11,16], [0.55, 0.55], 'g--', lw=4)
    plt.plot([11,16], [1.0, 1.0], 'b--', lw=4)

    if yscale == 'log':
        plt.semilogy()
        tick_locations = [0.01, 0.1, 0.55, 1.0, 10, 100]
        hist_bins = np.logspace(-2,2,50)
        hist_range=[0.01,100]
    else:
        tick_locations = [-1, 0, 0.55, 1.0, 2, 3, 4, 5]
        hist_bins=40
        hist_range=[-1,5]

    tick_labels = [str(x) for x in tick_locations]
    
    plt.xlabel("median $H$ mag")
    plt.ylabel("Stetson index")

    plt.title(title)

    ax_hist = fig.add_axes( (0.725, 0.1, 0.175, 0.8), sharey=ax_plot )

    plt.hist(autocan_strict.Stetson, 
             bins=hist_bins,
             range=hist_range,
             orientation='horizontal', color='r')
    plt.plot([0,1000], [0.55, 0.55], 'g--', lw=4, scalex=False)
    plt.plot([0,1000], [1.0, 1.0], 'b--', lw=4, scalex=False)

    plt.setp(ax_hist.get_xticklabels(), visible=False)
    plt.yticks(tick_locations, tick_labels)
    ax_hist.yaxis.tick_right()

    plt.ylim(hist_range)
    
    plt.show()

    return fig

def f_simple_observing_log(offset=54034):
    """
    Makes a 1D observing log separated by JHK but not by tile.

    """

    fig = plt.figure()

    sub1= plt.subplot(3,1,1)

    j_table = band_cut(variables_photometry, 'j')
    h_table = band_cut(variables_photometry, 'h')
    k_table = band_cut(variables_photometry, 'k')

    j_dates = np.array(list(set(j_table.MEANMJDOBS)))
    h_dates = np.array(list(set(h_table.MEANMJDOBS)))
    k_dates = np.array(list(set(k_table.MEANMJDOBS)))

    plt.plot(j_dates - offset, np.ones(len(j_dates)) + 1/4, 'b.')
    plt.plot(h_dates - offset, np.ones(len(h_dates)), 'g.')
    plt.plot(k_dates - offset, np.ones(len(k_dates)) - 1/4, 'r.')

    plt.ylim(1/3,2-1/3)
    plt.xticks([54101-offset, 54282-offset, 
                54466-offset, 54648-offset,
                54832-offset],
                ["Jan 2007", "July 2007",
                 "Jan 2008", "July 2008",
                 "Jan 2009"], rotation=30, fontsize=18)

    plt.setp(sub1.get_yticklabels(), visible=False)

    plt.show()
    return fig

def f_comparison_observing_log():
    """
    Zoomed out timeline comparing us to CHS2001 and YSOVAR time coverage.

    """

    fig = plt.figure(figsize=(9,2.5))

    chs01_start = 51580 #2000 Feb 6 in MJD 
    chs01_end = 51639 # 2000 Apr 8 in MJD
    ysovar_spitzer_start = 55126 #2009 Oct 23 in MJD
    ysovar_spitzer_end = 55163 # 2009 Dec 1 in MJD
    ysovar_ukirt_start = 55123 #2009 Oct 20 in MJD
    ysovar_ukirt_end = 55185 # 2009 Dec 22
    ysovar_cfht_start = 55130 # 2009 Oct 27
    ysovar_cfht_end = 55142 # 2009 Nov 8

    j_wavelength = 1.1 #microns
    h_wavelength = 1.6
    ks_wavelength = 2.15
    k_wavelength = 2.2
    irac1_wavelength = 3.6
    irac2_wavelength = 4.5

    j_table = band_cut(variables_photometry, 'j')
    h_table = band_cut(variables_photometry, 'h')
    k_table = band_cut(variables_photometry, 'k')

    wfcam_j_dates = np.array(list(set(j_table.MEANMJDOBS)))
    wfcam_h_dates = np.array(list(set(h_table.MEANMJDOBS)))
    wfcam_k_dates = np.array(list(set(k_table.MEANMJDOBS)))


    # Our observations
    plt.plot(wfcam_j_dates, j_wavelength*np.ones_like(wfcam_j_dates), 'b.')
    plt.plot(wfcam_h_dates, h_wavelength*np.ones_like(wfcam_h_dates), 'g.')
    plt.plot(wfcam_k_dates, k_wavelength*np.ones_like(wfcam_k_dates), 'r.')

    # Carpenter
    plt.plot([chs01_start, chs01_end], [j_wavelength]*2, 'b',lw=4)
    plt.plot([chs01_start, chs01_end], [h_wavelength]*2, 'g', lw=4)
    plt.plot([chs01_start, chs01_end], [ks_wavelength]*2, 'r', lw=4)

    # YSOVAR
    # spitzer
    plt.plot([ysovar_spitzer_start, ysovar_spitzer_end], 
             [irac1_wavelength]*2, 'm', lw=4)
    plt.plot([ysovar_spitzer_start, ysovar_spitzer_end], 
             [irac2_wavelength]*2, 'k', lw=4)

    # UKIRT
    plt.plot([ysovar_ukirt_start, ysovar_ukirt_end], [j_wavelength]*2, 
             'b', lw=4)
    # CFHT
    plt.plot([ysovar_cfht_start, ysovar_cfht_end], [j_wavelength]*2, 
             'b', lw=4)
    plt.plot([ysovar_cfht_start, ysovar_cfht_end], [ks_wavelength]*2, 
             'r', lw=4)

    #    plt.gca().invert_yaxis()
    plt.ylabel("Wavelength (microns)")
    plt.ylim(6, 0.1)

    xticks_values = [51544, 51910, 52275, 52640, 53005,
                     53371, 53736, 54101, 54466, 54832, 55197]
    xticklabels_values = ["20%02d"%x for x in range(11)]

    plt.xticks(xticks_values[::2], xticklabels_values[::2])

    plt.title("History of IR monitoring campaigns in the ONC")

    plt.text(51550, 3, "Carpenter+2001")
    plt.text(55050, 0.8, "YSOVAR$^a$")
    plt.text(53960, 3, "This paper's contribution")

    plt.text(55230, 4.5, "[4.5]", color='k', size=16)
    plt.text(55230, 3.6, "[3.6]", color='m', size=16)
    plt.text(55200, 2.5, "$K_s$", color='r', size=16)
    plt.text(55230, 1.3, "$J$", color='b', size=16)

    plt.text(53900, 2.5, "$K$", color='red', size=16)
    plt.text(53900, 1.8, "$H$", color='green', size=16)
    plt.text(53915, 1.1, "$J$", color='blue', size=16)
    
    plt.show()

    return fig

def f_observing_log(title="Observing log for each tile, for each band"):
    """
    Makes a graphical observing log.

    """

    tile_tables = filter_by_tile()[0]

    fig = plt.figure()

    for i, tile_table in zip(range(len(tile_tables)), tile_tables):

        # How do we J slice? BAND CUT
        j_tile_table = band_cut(tile_table, 'j')
        h_tile_table = band_cut(tile_table, 'h')
        k_tile_table = band_cut(tile_table, 'k')

        j_dates = list(set(j_tile_table.MEANMJDOBS))
        h_dates = list(set(h_tile_table.MEANMJDOBS))
        k_dates = list(set(k_tile_table.MEANMJDOBS))

        plt.plot(j_dates, 5/4+i*np.ones(len(j_dates)), 'b.')
        plt.plot(h_dates, 1+i*np.ones(len(h_dates)), 'g.')
        plt.plot(k_dates, 3/4+i*np.ones(len(k_dates)), 'r.')

    plt.xlabel("Modified Julian Date")
    plt.ylabel("Tile #", rotation='horizontal')
    plt.title(title)

    plt.ylim(1-1/3, 16+1/3)

    return fig

def f_observing_map():
    """
    Makes a map of observations and how many J, H, K band datapoints
    each tile has.

    """

    max_ra = maxvars.RA.max()
    min_ra = maxvars.RA.min()
    max_dec = maxvars.DEC.max()
    min_dec = maxvars.DEC.min()

    tile_size_ra = (max_ra - min_ra) / 4
    tile_size_dec = (max_dec - min_dec) / 4

    tile_spreadsheets = filter_by_tile()[1]

    fig = plt.figure(figsize=(6,6))

    ij_list = [(x, y) for x in range(4) for y in range(4)]

    text_params = {'horizontalalignment':'center',
                   'verticalalignment':'center'}

    # print the nice text and stuff
    for k, ij, tile_spreadsheet in zip(range(len(tile_spreadsheets)),
                                       ij_list, tile_spreadsheets):

        ra_i, dec_j = ij

        tile_ra = min_ra + tile_size_ra*ra_i + tile_size_ra/2
        tile_dec = min_dec + tile_size_dec*dec_j + tile_size_dec/2

        plt.text(np.degrees(tile_ra), np.degrees(tile_dec+tile_size_dec/4),
                 "Tile #%d" % (k+1), **text_params)
        plt.text(np.degrees(tile_ra), np.degrees(tile_dec+tile_size_dec/12),
                 "J: %3d" % tile_spreadsheet.N_j.max(), color='b',
                 **text_params)
        plt.text(np.degrees(tile_ra), np.degrees(tile_dec-tile_size_dec/12),
                 "H: %3d" % tile_spreadsheet.N_h.max(), color='g',
                 **text_params)
        plt.text(np.degrees(tile_ra), np.degrees(tile_dec-tile_size_dec/4),
                 "K: %3d" % tile_spreadsheet.N_k.max(), color='r', 
                 **text_params)


    physical_tile_size_ra = (max_ra - min_ra) / 3.88
    physical_tile_size_dec = (max_dec - min_dec) / 3.88

    # make the overlapping rectangles
    for k, ij in zip(range(len(ij_list)), ij_list):

        ra_i, dec_j = ij

        southeast_corner_ra = min_ra + 0.94*physical_tile_size_ra*ra_i
        southeast_corner_dec = min_dec + 0.94*physical_tile_size_dec*dec_j

        if ij == (0,0) or ij == (0,2) or ij == (2,0) or ij == (2,2):
            rectangle_params = {'color': '0.85',
                                'zorder':-10}
        else:
            rectangle_params = {'fill': False}
        
        plt.gca().add_patch(
            plt.Rectangle((np.degrees(southeast_corner_ra), 
                           np.degrees(southeast_corner_dec)),
                          np.degrees(physical_tile_size_ra), 
                          np.degrees(physical_tile_size_dec),
                          ec='k', **rectangle_params))

    northeast_corner = (np.degrees(maxvars.RA.max() + 0.001),
                        np.degrees(maxvars.DEC.max() + 0.001))

    southwest_corner = (np.degrees(maxvars.RA.min() - 0.001),
                        np.degrees(maxvars.DEC.min() - 0.001))    

    plt.xlim(northeast_corner[0], southwest_corner[0])
    plt.ylim(southwest_corner[1], northeast_corner[1])

    plt.xlabel("RA (deg)")
    plt.ylabel("Dec (deg)")

    return fig

def f_sensitivity_per_band():
    """
    Plots the observed rms versus magnitude for J, H, K.

    """

    fig = plt.figure()

    j_minimum = minimum.where((minimum.N_j > 50) & (minimum.Stetson < 0.5))
    h_minimum = minimum.where((minimum.N_h > 80) & (minimum.Stetson < 0.5))
    k_minimum = minimum.where((minimum.N_k > 80) & (minimum.Stetson < 0.5))

    s1 = plt.subplot(3,1,1)
    s2 = plt.subplot(3,1,2, sharex=s1)
    s3 = plt.subplot(3,1,3, sharex=s1)
    
    s1.plot(j_minimum.j_meanr, j_minimum.j_rmsr, 'b,')
    s2.plot(h_minimum.h_meanr, h_minimum.h_rmsr, 'g,')
    s3.plot(k_minimum.k_meanr, k_minimum.k_rmsr, 'r,')

    plt.xlim(10.5, 17.5)

    s3.set_xlabel("Magnitude")
    for s in [s1,s2,s3]:
        s.set_ylim(0,0.1)
        s.set_yticks([0, 0.05, 0.1])

    plt.show()

    return fig
    

#outdated
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
