"""
This is a SCRIPT that addresses two questions raised by Scott Wolk:

1. What are the variability properties in our data of previously known 
   YSOs, divided (by either/both X-ray or IR data) into CI, CII, 
   CIII categories,

and 

2. What do period distributions look like for disked, not-disked, and 
   extreme NIR color categories?

"""

import matplotlib.pyplot as plt

from tablemate_comparisons import ukvar_spread as ukvar_s
from tablemate_comparisons import ukvar_periods
from plot2 import plot_trajectory_vanilla
from tablemate_script import (XMM_north, XMM_north_c1, 
                              XMM_north_c2, XMM_north_c3,
                              Megeath2012, Megeath_P, Megeath_D)
from orion_tablemate import tablemater, TableParameters
from official_star_counter import autocan_strict, autocan_true

# We'll be "mating" these tables to the XMM data.
Ukirt_autocan_strict = TableParameters(
    data = autocan_strict,
    alias = "UKIRT_autocan_strict_allstars",
    full_name = "Master spreadsheet for 2436 stars in the UKIRT data that have 'pristine' data quality in all 3 bands.",
    ra_cols = ['RA'], dec_cols=['DEC'],
    radec_fmt = 'decimal-radians',
    name_col = 'SOURCEID')
    
Ukirt_autocan_true = TableParameters(
    data = autocan_true,
    alias = "UKIRT_autocan_true_allstars",
    full_name = "Master spreadsheet for 3705 stars in the UKIRT data that have 'pristine' data quality in at least 1 band.",
    ra_cols = ['RA'], dec_cols=['DEC'],
    radec_fmt = 'decimal-radians',
    name_col = 'SOURCEID')

ukirt_list = [Ukirt_autocan_strict, Ukirt_autocan_true]

# I'll wanna include UKvars at some point, too.
# Now let's do question one.

def match_xmm_to_ukirt():
    """ 
    A function that performs an "inverse" cross-match between 
    X-ray selected sources from XMM, and our UKIRT stars.

    """

    # Produces a table of cross-match IDs and indices.
    mated_xmm = tablemater(XMM_north, ukirt_list)
    
    mated_c1 =  tablemater(XMM_north_c1, ukirt_list)
    mated_c2 =  tablemater(XMM_north_c2, ukirt_list)
    mated_c3 =  tablemater(XMM_north_c3, ukirt_list)

    mated_list = [mated_xmm, mated_c1, mated_c2, mated_c3]

    # What kinds of plots do we want?
    # Histogram of S, for each xray category (incl. "all")
    fig = plt.figure()

    uks_i = 'UKIRT_autocan_strict_allstars_index'
    uks_d = autocan_strict

    uka_i = 'UKIRT_autocan_true_allstars_index'
    uka_d = autocan_true

    s1 = plt.subplot(4,1,1)
    s2 = plt.subplot(4,1,2)
    s3 = plt.subplot(4,1,3)
    s4 = plt.subplot(4,1,4)

    subplot_list = [s1, s2, s3, s4]
    name_list = ["all XMM sources",
                 "Class 1 XMM sources",
                 "Class 2 XMM sources",
                 "Class 3 XMM sources"]

    for s, m, name in zip(subplot_list, mated_list, name_list):
        # in approximate english: "the stats table, where you take the row 
        # handed to you by the mated table, but only where there's a match"
        try:
            # AUTO
            s.hist( 
                uka_d.Stetson[ 
                    m.where(m[uka_i] != -1)[uka_i] 
                    ], 
                range=[0,5], bins=20, color='b', label="1-band pristine"
                )
        except: pass
        try:
            # STRICT
            s.hist( 
                uks_d.Stetson[ 
                    m.where(m[uks_i] != -1)[uks_i] 
                    ], 
                range=[0,5], bins=20, color='r', label="3-band pristine"
                )
        except: pass

        # annotate each subplot so they're readable
        if s == s1:
            s.text(0.35, 0.75, name, transform=s.transAxes)
        else:
            s.text(0.65, 0.75, name, transform=s.transAxes)
        

    s1.set_title("Histogram: Stetson indices of X-ray-selected stars in ONC")
    s1.legend()
    s4.set_xlabel("Stetson Index")
    plt.show()


    # Now, I want to print out some stats relevant to what we want.
    # Think of how "official_star_counter" works.

    # For each group, print the stuff.

    for s, m, name in zip(subplot_list, mated_list, name_list):
        # Mean S and Variance?
        auto_stetson = uka_d.Stetson[m.where(m[uka_i] != -1)[uka_i]]
        strict_stetson = uks_d.Stetson[m.where(m[uks_i] != -1)[uks_i]]

        print ("%s Mean Stetson for auto-stars: %.3f +- %.2f" % 
               (name, auto_stetson.mean(), auto_stetson.std()))
        print ("%s Mean Stetson for strict-stars: %.3f +- %.2f" % 
               (name, strict_stetson.mean(), strict_stetson.std()))
        
    for s, m, name in zip(subplot_list, mated_list, name_list):
        # Mean Delta Mag (and sigmas)?
#        auto_delta = uka_d.[m.where(m[uka_i] != -1)[uka_i]]# doesn't quite work
        strict_delta = uks_d.k_range[m.where(m[uks_i] != -1)[uks_i]]

        print ("%s Mean delta-K (max-min) for strict-stars: %.3f +- %.2f" % 
               (name, strict_delta.mean(), strict_delta.std()))


        # What fraction have good periods? Not answerable right now.

    return mated_xmm, mated_c1, mated_c2, mated_c3

def match_spitzer_to_ukirt():
    """ 
    A function that performs an "inverse" cross-match between 
    mid-IR selected sources from Spitzer/Megeath2012, and our UKIRT stars.

    """

    # Produces a table of cross-match IDs and indices.
    mated_spitzer = tablemater(Megeath2012, ukirt_list)
    
    # Clearly, we need to update this to use slices of the Megeath table
    # filtered on Class.
    mated_P =  tablemater(Megeath_P, ukirt_list)
    mated_D =  tablemater(Megeath_D, ukirt_list)

    mated_list = [mated_spitzer, mated_P, mated_D]

    # What kinds of plots do we want?
    # Histogram of S, for each IR category (incl. "all")
    fig = plt.figure()

    uks_i = 'UKIRT_autocan_strict_allstars_index'
    uks_d = autocan_strict

    uka_i = 'UKIRT_autocan_true_allstars_index'
    uka_d = autocan_true

    s1 = plt.subplot(3,1,1)
    s2 = plt.subplot(3,1,2)
    s3 = plt.subplot(3,1,3)

    subplot_list = [s1, s2, s3]
    name_list = ["all Spitzer YSO sources",
                 "Spitzer Protostars",
                 "Spitzer Disked sources"]

    for s, m, name in zip(subplot_list, mated_list, name_list):
        # in approximate english: "the stats table, where you take the row 
        # handed to you by the mated table, but only where there's a match"
        try:
            # AUTO
            s.hist( 
                uka_d.Stetson[ 
                    m.where(m[uka_i] != -1)[uka_i] 
                    ], 
                range=[0,5], bins=20, color='b', label="1-band pristine"
                )
        except: pass
        try:
            # STRICT
            s.hist( 
                uks_d.Stetson[ 
                    m.where(m[uks_i] != -1)[uks_i] 
                    ], 
                range=[0,5], bins=20, color='r', label="3-band pristine"
                )
        except: pass

        # annotate each subplot so they're readable
        if s == s1:
            s.text(0.25, 0.75, name, transform=s.transAxes)
        else:
            s.text(0.65, 0.75, name, transform=s.transAxes)
        

    s1.set_title("Histogram: Stetson indices of Spitzer-selected stars in ONC")
    s1.legend()
    s3.set_xlabel("Stetson Index")
    plt.show()


    # Now, I want to print out some stats relevant to what we want.
    # Think of how "official_star_counter" works.

    # For each group, print the stuff.

    for s, m, name in zip(subplot_list, mated_list, name_list):
        # Mean S and Variance?
        auto_stetson = uka_d.Stetson[m.where(m[uka_i] != -1)[uka_i]]
        strict_stetson = uks_d.Stetson[m.where(m[uks_i] != -1)[uks_i]]

        print ("%s Mean Stetson for auto-stars: %.3f +- %.2f" % 
               (name, auto_stetson.mean(), auto_stetson.std()))
        print ("%s Mean Stetson for strict-stars: %.3f +- %.2f" % 
               (name, strict_stetson.mean(), strict_stetson.std()))
        
    for s, m, name in zip(subplot_list, mated_list, name_list):
        # Mean Delta Mag (and sigmas)?
#        auto_delta = uka_d.[m.where(m[uka_i] != -1)[uka_i]]# doesn't quite work
        strict_delta = uks_d.k_range[m.where(m[uks_i] != -1)[uks_i]]

        print ("%s Mean delta-K (max-min) for strict-stars: %.3f +- %.2f" % 
               (name, strict_delta.mean(), strict_delta.std()))


        # What fraction have good periods? Not answerable right now.

    # Finally, let's make a plot of S vs alpha_irac.
    fig2 = plt.figure()

    # define the Stetson column and the alpha_irac column
    m = mated_spitzer

    meg_i = 'Megeath2012_index'
    meg_d = Megeath2012.data

    auto_alpha_irac = meg_d.alpha[m.where(
            m[uka_i] != -1)[meg_i] ]
    strict_alpha_irac = meg_d.alpha[m.where(
            m[uks_i] != -1)[meg_i] ]

    auto_stetson = uka_d.Stetson[m.where(m[uka_i] != -1)[uka_i]]
    strict_stetson = uks_d.Stetson[m.where(m[uks_i] != -1)[uks_i]]

    plt.plot( auto_alpha_irac, auto_stetson, 'bo', label="1-band pristine")
    plt.plot( strict_alpha_irac, strict_stetson, 'ro', label="3-band pristine")
        
    plt.legend()

    plt.xlabel(r"Spectral index $\alpha_{IRAC}$", fontsize=18)
    plt.ylabel("Stetson Index", fontsize=18)

    plt.title(r"Stetson vs $\alpha$ for Spitzer-selected sources")

    plt.show()

    print auto_alpha_irac

    return mated_spitzer, mated_P, mated_D


# crude copy
ukvar_spread = ukvar_s.where(ukvar_s.SOURCEID > 0)

ukvar_spread.add_column('Period', ukvar_periods)

# Let's do question two first.

# so... disk selection works like this:
# if 
#    (J-H) > 1.714*(H-K) 
# then it's a "photosphere"
# if 
#    (J-H) < 1.714*(H-K) and (J-H) > 1.714*(H-K)-0.614 
# then it's a "disk"
# if
#    (J-H) > 1.714*(H-K)-0.614 
# then it's an "extreme disk".

# The population that we're drawing from is "strict periodics" and/or
# 'ukvar.where(ukvar.strict + ukvar.periodic == 2)
# and we're gonna need ukvar_periods as well

def period_disk_class_histograms():
    """ 
    What do the period distributions of disked vs nondisked stars look like?

    """

    # UKvar sTrict Periodics
    uk_tp = ukvar_spread.where((ukvar_spread.strict == 1) & 
                               (ukvar_spread.periodic == 1))

    # Disk criterion
    excess = 1.714*uk_tp.hmk_median - uk_tp.jmh_median 

    p_sample = uk_tp.where(excess <= 0)
    d_sample = uk_tp.where((excess > 0) & (excess <= 0.614))
    e_sample = uk_tp.where(excess > 0.614)

    print len(p_sample), len(d_sample), len(e_sample)

    fig = plt.figure()
    s1 = fig.add_subplot(3,1,1)
    s2 = fig.add_subplot(3,1,2)
    s3 = fig.add_subplot(3,1,3)

    s1.hist(p_sample.Period, bins=50, range=(0,20))
    s1.text(12,10, "Photosphere sample, n=%d" % len(p_sample))
    s1.set_title("Histograms of periods for photosphere, disk, extreme samples")
    s2.hist(d_sample.Period, bins=50, range=(0,20),color='r')
    s2.text(12,10, "Disk sample, n=%d" % len(d_sample))
    s3.hist(e_sample.Period, bins=50, range=(0,20),color='k')
    s3.text(12,0.8, "Extreme sample, n=%d" % len(e_sample))
    s3.set_xlabel("Period (days)")

    plt.show()

    fig2 = plt.figure()

    plot_trajectory_vanilla(plt.gca())
    
    plt.plot(p_sample.hmk_median, p_sample.jmh_median, 'bo')
    plt.plot(d_sample.hmk_median, d_sample.jmh_median, 'ro')
    plt.plot(e_sample.hmk_median, e_sample.jmh_median, 'ko')

    plt.xlabel(r"median $H-K$")
    plt.ylabel(r"median $J-H$")
    plt.title("Color-color diagram of periodic stars")

    plt.xlim(-0.1,2.5)
    plt.ylim(-0.2, 2.8)

    plt.show()

    return
