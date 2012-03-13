''' 
A python module to compare the global photometric fidelity between 
nights in WSA data and remove nights whose data are obviously 
affected by processing errors or unfavorable observing conditions.

Written by Tom Rice, September 2011.
t.rice90@gmail.com

2011-09-16 00:10 TSR: Created.
2011-09-28 01:45 TSR: Polished up and completed.
2012-03-13 15:18 TSR: Adapting to the Orion dataset.

analyze_nights2 and remove_nights2 are the preferred versions.

'''

import numpy as np
import atpy
import matplotlib.pyplot as plt
import robust as rb




''' Example call:

data = atpy.Table('full_data.fits')
whale = analyze_nights(data)
shark = remove_nights(data, whale)
'''

def analyze_nights2 (table,  
                     jbright=13, jdim=18,
                     hbright=12, hdim=17,
                     kbright=11.5, kdim=16.5) :
    '''
    A function that calculates the mean stellar color
    on each night, and selects outliers.

    Takes a while to run. (over 2 minutes on my machine)

    Hacked on some things to deal with the fact that chipset #1 is missing 
    a night. Only runs on the intact downloaded dataset.

    Parameters
    ----------
    table : atpy.Table
        a data table of time-series photometry from the WFCAM
        Science Archive (WSA). Must include all magnitudes, colors,
        color errors, ppErrBits, and MeanMjdObs information.

    Returns
    -------
    divvied : list of ndarray
        Four arrays corresponding to all the timestamps of each
        chipset.
    mean_hmk : 2-D ndarray 
    mean_jmh : 2-D ndarray
        
    '''
    
    # We want 4 arrays, one corresponding to each chipset.

    n_timestamps = len(list(set(table.MEANMJDOBS)))
    n_nights = np.ceil( n_timestamps / 4.)
    
    mean_hmk =  np.zeros(( 4, n_nights ))
    mean_jmh =  np.zeros(( 4, n_nights ))
 
    
    # Let's divvy up the timestamps into 4 arrays.
    # Every night has 4 timestamps except the final one. 
    # (I confirmed this empirically)
    # NO YOU DIDN'T TOM, YOU WERE WRONG
    # To correct for this failure, here's a thing:
    timestamps = np.array(sorted(list(set(table.MEANMJDOBS))))

    if timestamps.size != 496:

        dummy_night = 54920
        timestamps = np.array(sorted(list(set(table.MEANMJDOBS))+[dummy_night]))

    print timestamps.size

    times1 = timestamps[ np.arange(0, n_timestamps, 4)]
    times2 = timestamps[ np.arange(0, n_timestamps, 4)+1]
    times3 = timestamps[ np.arange(0, n_timestamps, 4)+2]
    times4 = timestamps[ np.arange(0, n_timestamps, 4)+3]

    divvied = [times1,times2,times3,times4]

    # Loop a bunch.

    # First, over chipsets:
    for i in range(4):

        print i
        # Then over timestamps
        for (j, time) in zip(range(n_nights), divvied[i]):
            
            # Calculate and save

            # Let's trim out all the obviously bad data, as well as the
            # suspicious data. This means aiming for between mags 11 and 18,
            # and removing ALL pperrbits.

            this_night = table.where(table.MEANMJDOBS == time)

            good = this_night.where( (this_night.JAPERMAG3 > jbright) &
                                     (this_night.JAPERMAG3 < jdim) &
                                     (this_night.HAPERMAG3 > hbright) &
                                     (this_night.HAPERMAG3 < hdim) &
                                     (this_night.KAPERMAG3 > kbright) &
                                     (this_night.KAPERMAG3 < kdim) &
                                     (this_night.JPPERRBITS < 5) &
                                     (this_night.HPPERRBITS < 5) &
                                     (this_night.KPPERRBITS < 5) )

            
            mean_hmk[i,j] = good.HMKPNT.mean()
            mean_jmh[i,j] = good.JMHPNT.mean()



    print "made it this far"
            

    return (divvied, mean_hmk, mean_jmh)


def remove_nights2 (table, analysis):
    '''
    Removes nights from a table based on the output 
    of analyze_nights2.

    Must be called after analyze_nights2.

    Parameters
    ----------
    table : atpy.Table
        a data table of time-series photometry from the WFCAM
        Science Archive (WSA). Must include all magnitudes, colors,
        color errors, ppErrBits, and MeanMjdObs information.
    analysis : tuple
        The output of analyze_nights2.

    Returns
    -------
    newtable : atpy.Table
        The same data table, with all data from bad nights
        removed.
    badnights : ndarray
        The list of timestamps that were rejected.
    cuts : list of tuples
        The parameters used for rejecting nights. 
        Order of each tuple: 
        (mean_hmk, mean_jmh, spread_hmk, spread_jmh)
        
    '''

    # First, let's relabel analyze_nights2' output.
    
    nights, hmk, jmh = analysis #this depends on what analyze_nights outputs

    master_cloudy = []

    cuts = []
    
    for night_set, mean_hmk, mean_jmh in zip(nights, hmk, jmh):

        # Let's call in the big guns... robust statistics and outlier clipping
        # or, you know, some way to return the outliers.
        # Get the robust standard deviation and then write down everyone above.

        middle_hmk = rb.meanr(mean_hmk)
        middle_jmh = rb.meanr(mean_jmh)

        spread_hmk = rb.stdr(mean_hmk)
        spread_jmh = rb.stdr(mean_jmh)

        ellipse = np.sqrt( ((mean_hmk - middle_hmk)/spread_hmk)**2 +
                           ((mean_jmh - middle_jmh)/spread_jmh)**2 )

        cloudy = night_set[ ellipse > 3 ]
        
        print "let's test this."
        print "middle: ", middle_hmk
        print "spread: ", spread_hmk
        print "n_outliers: ", cloudy.size

        # now let's save cloudy
        master_cloudy.extend(cloudy)
        
        cuts.append((middle_hmk, middle_jmh,
                     spread_hmk, spread_jmh))
        

    
    # now let's remove the nights
    clean_data = table.where( 
        np.array([night not in master_cloudy for night in table.MEANMJDOBS]) 
                  )

    return clean_data, master_cloudy, cuts

def simple_analyze (table) :
    '''
    Doesn't separate the nights into 4 different sets, 
    but can be used on a dataset that's missing timestamps
    (such as the output of remove_nights).
    
    "If you're not writing tests for your code, you should be 
    majoring in religion, not computer science"
    '''

    n_timestamps = len(list(set(table.MEANMJDOBS)))

    mean_hmk =  np.zeros( n_timestamps )
    mean_jmh =  np.zeros( n_timestamps )

    timestamps = np.array(sorted(list(set(table.MEANMJDOBS)) ))

    for (i, time) in zip(range(n_timestamps), timestamps):
        this_night = table.where(table.MEANMJDOBS == time)

        good = this_night.where( (this_night.JAPERMAG3 > 13) &
                                 (this_night.JAPERMAG3 < 18) &
                                 (this_night.HAPERMAG3 > 12) &
                                 (this_night.HAPERMAG3 < 17) &
                                 (this_night.KAPERMAG3 > 11.5) &
                                 (this_night.KAPERMAG3 < 16.5) &
                                 (this_night.JPPERRBITS < 5) &
                                 (this_night.HPPERRBITS < 5) &
                                 (this_night.KPPERRBITS < 5) )

        
        mean_hmk[i] = good.HMKPNT.mean()
        mean_jmh[i] = good.JMHPNT.mean()

    return timestamps, mean_hmk, mean_jmh
