"""
A module for retrieving SIMBAD names for stars.

Uses astroquery.simbad; is fairly straighforward.

"""

import numpy as np
import astroquery.simbad

def simbad_namer(table, max_match=1., radec_fmt = 'rad'):
    """
    Matches all sources to SIMBAD names.

    Parameters
    ----------
    table : atpy.Table
        Table containing RA, Dec of desired source matches.
    max_match : float, optional
        Maximum match in arcseconds.
    radec_fmt : {'rad'|'dec'}, optional
        What format are the RA and DEC columns of `table` in?

    Returns
    -------
    simbad_names : np.ndarray of str

    """

    if 'rad' in radec_fmt.lower():
        ra_col = np.degrees(table.RA)
        dec_col = np.degrees(table.DEC)
    else:
        ra_col = table.RA
        dec_col = table.DEC

    name_list = []

    for ra, dec in zip(ra_col, dec_col):
        al = astroquery.simbad.QueryCoord(ra=ra, dec=dec, 
                                          radius=str(max_match)+"s").execute()
        try: 
            name_list.append( al.table['MAIN_ID'][0] )
        except Exception, e: 
            print e
            name_list.append( "" )

    # Now let's cast to an array so that we can append it to an atpy.Table
    simbad_names = np.array(name_list)

    return simbad_names
