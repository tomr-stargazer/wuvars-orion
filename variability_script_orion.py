""" This is a script (not a program!) that uses my functions to quantify variability for my stars. """

import numpy as np
import atpy
import spread3 as sp
import datetime

print "Hey, just a heads-up, this is an INTERACTIVE script."
print " You should call the following functions:"
print " -test() # To make sure everything's working fine"
print "         # before wasting a lot of time."
print " -calculate_stuff() # To calculate stuff."
print " -glue_stuff() # To glue together the calculated stuff."
print "               # Note, this one returns the spreadsheet."
print ""
print "New feature: you can pass a number to calculate_stuff() and glue_stuff()"
print "(such as 25, 50, 100) as a manual control on how many chunks to split"
print "the data into. Make sure to use the same number for both functions!!"

path = '/home/tom/reu/ORION/DATA/'
path2= path+'spreadsheet/'

data = atpy.Table('/home/tom/reu/ORION/DATA/fde_graded_clipped0.8_scrubbed0.1.fits')
#data = atpy.Table('/home/tom/reu/ORION/DATA/constantstars_073112_data_errorcorrected.fits')
#data = atpy.Table('/home/tom/reu/ORION/DATA/full_data_errorcorrected.fits')
#data = atpy.Table('/home/tom/reu/ORION/DATA/s3_photometric_errorcorrected.fits')
print "old data size is ", data.shape

# First, let's select a certain part of the data, to trim it down.
# This cuts the data size in half!

# Actually, let's not do that.

#data = data.where((data.JAPERMAG3 < 17.3) & ( data.JAPERMAG3 > 9.7) & (
#        data.HAPERMAG3 < 16.3) & ( data.HAPERMAG3 > 9.7) & (
#        data.KAPERMAG3 < 16.3) & ( data.KAPERMAG3 > 9.7) )

print "new data size is ", data.shape

# Fix the data by correcting the errors!

# s = 0.021
# c = 1.082

# data.JAPERMAG3ERR = np.sqrt( c*data.JAPERMAG3ERR**2 + s**2)
# data.HAPERMAG3ERR = np.sqrt( c*data.HAPERMAG3ERR**2 + s**2)
# data.KAPERMAG3ERR = np.sqrt( c*data.KAPERMAG3ERR**2 + s**2)

# data.JMHPNTERR = np.sqrt( c*data.JMHPNTERR**2 + s**2)
# data.HMKPNTERR = np.sqrt( c*data.HMKPNTERR**2 + s**2)

def test():
    ''' Runs spread_write_test. '''
    sp.spread_write_test (data, sp.base_lookup(data))

def calculate_stuff( splits = 10 ):
    ''' 
    Runs the spreadsheet, first splitting it into `splits` 
    spreadsheets and then joining them. 
    
    '''
    
    if type(splits) is not int:
        raise TypeError

# We are going to split this into 10 smaller pieces through the magic of mod operations! woo.
    
    split_data = []
    spreadsheets = []

    for i in range(splits):
        data_i = data.where(data.SOURCEID % splits == i)
        
        split_data.append(data_i)
        
        lookup_i = sp.base_lookup(data_i)
        
        # The parameter "-1" is the season that tells data_cut not to make 
        # any cuts on the data.
        sp_i = sp.spreadsheet_write(data_i, lookup_i, -1, 
                                    path2+'sp%d.fits'%i, flags=256,
                                    graded=True)
        
        try:
            now = datetime.datetime.strftime(datetime.datetime.now(),
                                             "%Y-%m-%d %H:%M:%S")
        except:
            now = 'sometime'
        print "finished chunk %d at %s" % (i, now)
                                           


def glue_stuff( splits = 10 ):
    ''' Read in the tables from earlier and glue them together '''

    if type(splits) is not int:
        raise TypeError

    spread = atpy.Table(path2+'sp0.fits')
    
    spread_list = []
 
    for i in range(1,splits):
        other_spread = atpy.Table(path2+'sp%d.fits' %i )
        spread.append(other_spread) 


    return spread
        
#    for i in range(1,splits):
#        spread_list.append( atpy.Table('sp'+str(i)))

    

    
