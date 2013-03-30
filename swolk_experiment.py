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
