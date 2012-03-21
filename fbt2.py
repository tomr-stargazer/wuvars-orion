''' 
A python module to compare the global photometric fidelity between 
nights in WSA data and remove nights whose data are obviously 
affected by processing errors or unfavorable observing conditions.

This is a procedure to find bad timestamps. 
It is different from "find_bad_timestamps" 
and is therefore named fbt2.

The principle is to take "constant" stars, compute the offsets 
of each from their mean magnitude, and STACK THEM ALL TOGETHER. 
Nights that are offset from zero will stand out like a 
sore thumb, hopefully.

Of course, the definition of "constant" stars may already be 
prey to these bad nights, so one can never really know. But whatevs.

Written by Tom Rice, March 2012.
t.rice90@gmail.com

2012-03-20 14:39 TSR: Created.
'''

def stacker(odata, lookup):
    ''' Stacks lightcurves for constant stars and outputs the stacked LC.

    Inputs:
      - data: an ATpy table with lightcurve data
      - lookup: a variability stats table (spreadsheet) with only data 
                on "constant" stars.

    Outputs:
      - out_table: an ATpy table with columns corresponding to 
                   MEANMJDOBS, JAPERMAG3, HAPERMAG3, and KAPERMAG3
                   showing the stacked offset for each night.
                   Then we can clip them!
    '''
   
    # Let's remove all the non-constant-star photometry
    print "old size is ", data.shape
    data = odata.where(np.array([i in data.SOURCEID for i in lookup.SOURCEID]))
    print "new size is ", data.shape
    
    # Now let's compute the deviations for each star
    j_dev = np.ones_like(data.JAPERMAG3)
    h_dev = np.ones_like(data.JAPERMAG3)
    k_dev = np.ones_like(data.JAPERMAG3)
    data.add_column("JDEV", j_dev)
    data.add_column("HDEV", h_dev)
    data.add_column("KDEV", k_dev)
    
    for s in lookup.SOURCEID:
        jmean = lookup.j_mean[s == lookup.SOURCEID]
        hmean = lookup.h_mean[s == lookup.SOURCEID]
        kmean = lookup.k_mean[s == lookup.SOURCEID]
        sdata = np.array(data.SOURCEID == s)

        # We're going to choose, right here, our sign convention
        data.JDEV[sdata] = data.JAPERMAG3[sdata] - jmean
        data.HDEV[sdata] = data.HAPERMAG3[sdata] - hmean
        data.KDEV[sdata] = data.KAPERMAG3[sdata] - kmean
        
    # So, we need to know what the timestamps are 
    # (and it helps if they are sorted)
    timestamps = np.array(sorted(list(set(table.MEANMJDOBS))))

    j_dev_stack = np.zeros_like(timestamps)
    h_dev_stack = np.zeros_like(timestamps)
    k_dev_stack = np.zeros_like(timestamps)

    j_dev_sig = np.zeros_like(timestamps)
    h_dev_sig = np.zeros_like(timestamps)
    k_dev_sig = np.zeros_like(timestamps)

    # Now let's loop through every night and grab data from all the 
    # constant stars
    for (i, time) in zip(range(len(timestamps)), timestamps):
        
        tdata = np.array(data.MEANMJDOBS == time)
        
        j_dev_stack = np.sum( data.JDEV[tdata] )
        h_dev_stack = np.sum( data.HDEV[tdata] )        
        k_dev_stack = np.sum( data.KDEV[tdata] )

        j_dev_sig = np.std( data.JDEV[tdata] )
        h_dev_sig = np.std( data.HDEV[tdata] )        
        k_dev_sig = np.std( data.KDEV[tdata] )


        pass
    
    # and then create an output table to put it all.
    # with columns for date, stacked jdev, hdev, kdev.
    # And maybe some comments about how it was made?
    
    out = atpy.Table()
    out.add_column("MEANMJDOBS", timestamps)
    out.add_column("JAPERMAG3", j_dev_stack)
    out.add_column("JAPERMAG3ERR", j_dev_sig)
    out.add_column("HAPERMAG3", h_dev_stack)
    out.add_column("HAPERMAG3ERR", h_dev_sig)
    out.add_column("KAPERMAG3", k_dev_stack)
    out.add_column("KAPERMAG3ERR", k_dev_sig)

    return out


#def remover(
