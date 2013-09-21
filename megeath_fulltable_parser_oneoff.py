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

import atpy

dropbox_aux_catalogs = os.path.expanduser("~/Dropbox/Bo_Tom/aux_catalogs/")

def get_full_megeath_table():
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

    for column_name, i in zip(column_names, range(len(column_names))):
        addc(column_name, megeath_fulltable_idl.ctotal[:,i])

    return table
