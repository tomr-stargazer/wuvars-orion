"""
Parses the "full" Megeath Spitzer table of 306162 sources in Orion.

Downloaded from http://astro1.physics.utoledo.edu/~megeath/Orion/The_Spitzer_Orion_Survey.html

see README: http://astro1.physics.utoledo.edu/~megeath/orion/readme_spitzer_082112

in particular,
"ctotal" is the array of coordinates and photometry in the following format, RA, Dec, J, H, Ks, 3.6, 4.5, 5.8, 8, 24, uncJ, uncH,............unc24 

"""


def get_full_megeath_table():
    """
    Turns the Megeath table into an ATpy table.

    Truncated by RA, Dec to make matching easier.

    """

    
