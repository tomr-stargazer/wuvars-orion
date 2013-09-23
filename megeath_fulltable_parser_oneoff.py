"""
Parses the "full" Megeath Spitzer table of 306162 sources in Orion.

Downloaded from http://astro1.physics.utoledo.edu/~megeath/Orion/The_Spitzer_Orion_Survey.html

see README: http://astro1.physics.utoledo.edu/~megeath/orion/readme_spitzer_082112

in particular,
"ctotal" is the array of coordinates and photometry in the following format, RA, Dec, J, H, Ks, 3.6, 4.5, 5.8, 8, 24, uncJ, uncH,............unc24 

"""

from __future__ import division

import os
import scipy.io

import numpy as np

import atpy

dropbox_aux_catalogs = os.path.expanduser("~/Dropbox/Bo_Tom/aux_catalogs/")

# In [38]: np.degrees(ukvar_spread.RA).max()+0.001, 
#          np.degrees(ukvar_spread.RA).min()-0.001
# Out[38]: (84.260968502790917, 83.390274129869482)
max_RA = 84.261
min_RA = 83.39

# In [39]: np.degrees(ukvar_spread.DEC).max()+0.001, 
#          np.degrees(ukvar_spread.DEC).min()-0.001
# Out[39]: (-4.9666934580824265, -5.8535642750075771)
max_Dec = -4.96
min_Dec = -5.86

def clobber_table_write(table, filename, **kwargs):
    """ Writes a table, even if it has to clobber an older one. """

    try:
        table.write(filename, **kwargs)
    except Exception, e: 
        print e
        print "Overwriting file."
        os.remove(filename)
        table.write(filename, **kwargs)


def get_full_megeath_table(truncated=True):
    """
    Turns the Megeath table into an ATpy table.

    Truncated by RA, Dec to make matching easier.

    """

    # Read this guy in originally
    megeath_fulltable_idl = scipy.io.readsav(
        dropbox_aux_catalogs+'spitzer_orion_survey_082112.sav')

    # Make it into an ATpy table
    table = atpy.Table()
    table.table_name = 'Megeath full Spitzer catalog'

    addc = table.add_column

    column_names = ['RA', 
                    'Dec', 
                    'J',
                    'H',
                    'K',
                    '3.6', 
                    '4.5', 
                    '5.8', 
                    '8', 
                    '24', 
                    'e_J',
                    'e_H',
                    'e_K',
                    'e_3.6', 
                    'e_4.5', 
                    'e_5.8', 
                    'e_8', 
                    'e_24']

    addc('IDL_index', np.arange(len(megeath_fulltable_idl.ctotal[:,0])))

    for column_name, i in zip(column_names, range(len(column_names))):
        addc(column_name, megeath_fulltable_idl.ctotal[:,i])

    if truncated:
        truncated_table = table.where((table.RA < max_RA) & (table.RA > min_RA) &
                                      (table.Dec < max_Dec) & (table.Dec > min_Dec))
        
        return truncated_table
    else:
        return table

def write_full_megeath_table(truncated=True):
    """
    Writes the above table to the `dropbox_aux_catalogs` path.

    """

    table = get_full_megeath_table(truncated)

    if truncated:
        trunc_string = '_truncated'
    else:
        trunc_string = ''

    clobber_table_write(table, dropbox_aux_catalogs +
                'spitzer_orion_survey_082112%s.fits' % trunc_string)
