"""
This is a module that helps us dig for periods from the following catalogs:

GCVS (General Catalog of Variable Stars), as downloaded by me
Carpenter, Hillenbrand, Skrutskie 2001
YSOVAR: Morales-Calderon 2011
Herbst 2002
Parihar 2009

"""

import numpy as np

import atpy

# We'll import the tables of interest directly from tablemate_script

from tablemate_script import (GCVS, Carpenter_2001, 
                              YSOVAR_YSOs, YSOVAR_NoExcess,
                              Herbst2002, Parihar2009, dpath)

# and open up a couple new tables that have actual periods in them

Carpenter2001_periods = atpy.Table(dpath+"Carpenter2001_datafile7.txt", 
                                   type='ascii')
YSOVAR_periods = atpy.Table(dpath+"MoralesCalderon2011_table4.txt",
                            type='ascii')
Parihar2009_periods = atpy.Table(dpath+"Parihar2009_table5.fits")

RL2009_periods = atpy.Table(dpath+"RodriguezLedesma2009_table2.fits")

def GCVS_period_get(mated_table, primary_index, gcvs_direct=False):
    """ 
    Gets a period for an input star from the GCVS table.

    Parameters
    ----------
    mated_table : atpy.Table
        Output of tablemate_script containing desired sources.
        Must have a GCVS index column - this implies it was matched 
        to GCVS already.
    primary_index : int
        The index (starting at zero) of the input star, in the mated_table.
        Note: if `gcvs_direct` == True, then enter the desired star's 
        GCVS index here instead.
    gcvs_direct : bool, optional (default False)
        if True, then `mated_table` is disregarded and `primary_index` 
        is used as an index to the GCVS table directly.

    Returns
    -------
    gcvs_period : float or np.NaN
        The GCVS-listed Period for the input star.
        If the star is not in the GCVS, or does not have a listed period,
        then np.NaN is returned.

    """

    # fortunately, this one is as simple as asking the table 
    # for the Period value and returning it (or np.NaN, if we are handed a nan).

    if gcvs_direct:
        gcvs_index = primary_index
        if gcvs_index >= len(GCVS.data):
            return np.NaN
    # now we have to check to see if the source even has a GCVS match
    elif mated_table.GCVS_index[primary_index] == -1:
#        print "apparently, failure to match"
        return np.NaN
    else:
        gcvs_index = mated_table.GCVS_index[primary_index]

    gcvs_period = GCVS.data.Period[gcvs_index]

#    print gcvs_period
    
    if np.isnan(gcvs_period):
        return np.NaN
    else:
        return gcvs_period
    

def CHS01_period_get(mated_table, primary_index):
    """
    Gets a period for an input star from the Carpenter 2001 table.

    Parameters
    ----------
    mated_table : atpy.Table
        Output of tablemate_script containing desired sources.
        Must have a CHS01 index column - this implies it was matched
        to CHS01 already.
    primary_index : int
        The index (starting at zero) of the input star, in the mated_table.

    Returns
    -------
    chs_period : float or np.NaN
        The CHS01-listed Period for the input star.
        If the star is not in the CHS table, or does not have a listed period,
        then np.NaN is returned.

    """

    # For this function, it's a little more complicated since we have to
    # leapfrog from the Carpenter table straight to the separate period table
    # (namely, Table 7: `Carpenter2001_periods` in this script)

    chs_ID = mated_table.CHS2001_ID[primary_index]

    if chs_ID == -1:
        return np.NaN

    # should be unique, so [0][0] is justified, unless there's no match
    try:
        chs_p_index = np.where(Carpenter2001_periods.ID == chs_ID)[0][0]
    except IndexError, e:
        return np.NaN

    # grab the three periods, take the median - will probs be a safe bet
    chs_period = np.median((Carpenter2001_periods.PerJ[chs_p_index],
                            Carpenter2001_periods.PerH[chs_p_index],
                            Carpenter2001_periods.PerK[chs_p_index]))

    if chs_period > 0:
        return chs_period

def YSOVAR_period_get(mated_table, primary_index):
    """
    Gets a period for an input star from the YSOVAR Orion table.

    Parameters
    ----------
    mated_table : atpy.Table
        Output of tablemate_script containing desired sources.
        Must have YSOVAR index columns - this implies it was matched
        to the two YSOVAR tables already.
    primary_index : int
        The index (starting at zero) of the input star, in the mated_table.

    Returns
    -------
    ysovar_period : float or np.NaN
        The YSOVAR-listed Period for the input star.
        If the star is not in the YSOVAR tables, or does not have
        a listed period, then np.NaN is returned.

    """

    # For this function, it's even more complicated since there are
    # TWO Ysovar tables, and we're matching by an ID string rather than
    # an index!
    # (the period table is Table 7: `YSOVAR_periods` in this script)

    ysovar_yso_ID = mated_table.YSOVAR_OrionYSOs_ID[primary_index]
    ysovar_noex_ID = mated_table.YSOVAR_OrionNoExcess_ID[primary_index]

    if ysovar_yso_ID != '-1':
        ysovar_ID = ysovar_yso_ID
    elif ysovar_noex_ID != '-1':
        ysovar_ID = ysovar_noex_ID
    else:
        return np.NaN

    # should be unique, so [0][0] is justified, unless there's no match
    try:
        ysovar_p_index = np.where(YSOVAR_periods['Source^a'] == ysovar_ID)[0][0]
    except IndexError, e:
        return np.NaN

    ysovar_period = YSOVAR_periods['Period (days)'][ysovar_p_index]

    return ysovar_period


def Herbst_period_get(mated_table, primary_index, herbst_direct=False):
    """
    Gets a period for an input star from the Herbst 2002 table.

    Parameters
    ----------
    mated_table : atpy.Table
        Output of tablemate_script containing desired sources.
        Must have a Herbst index column - this implies it was matched
        to Herbst already.
    primary_index : int
        The index (starting at zero) of the input star, in the mated_table.
        Note: if `herbst_direct` == True, then enter the desired star's
        Herbst index here instead.
    herbst_direct : bool, optional (default False)
        if True, then `mated_table` is disregarded and `primary_index`
        is used as an index to the Herbst table directly.

    Returns
    -------
    herbst_period : float or np.NaN
        The Herbst2002-listed Period for the input star.
        If the star is not in the Herbst, or does not have a listed period,
        then np.NaN is returned.

    """
    # fortunately, this one is as simple as asking the table
    # for the Period value and returning it (or np.NaN, if we are handed a nan).

    if herbst_direct:
        herbst_index = primary_index
        if herbst_index >= len(Herbst2002.data):
            return np.NaN
    # now we have to check to see if the source even has a Herbst2002 match
    elif mated_table.Herbst2002_index[primary_index] == -1:
#        print "apparently, failure to match"
        return np.NaN
    else:
        herbst_index = mated_table.Herbst2002_index[primary_index]

    herbst_period = Herbst2002.data.Per[herbst_index]

#    print herbst_period

    if np.isnan(herbst_period):
        return np.NaN
    else:
        return herbst_period


def Parihar_period_get(mated_table, primary_index):
    """
    Gets a period for an input star from the Parihar 2009 table.

    Parameters
    ----------
    mated_table : atpy.Table
        Output of tablemate_script containing desired sources.
        Must have a Parihar09 index column - this implies it was matched
        to Parihar09 already.
    primary_index : int
        The index (starting at zero) of the input star, in the mated_table.

    Returns
    -------
    par_period : float or np.NaN
        The Parihar09-listed Period for the input star.
        If the star is not in the Par09 table, or does not have a listed period,
        then np.NaN is returned.

    """

    # For this function, it's a little more complicated since we have to
    # leapfrog from the Parihar table straight to the separate period table
    # (namely, Table 5: `Parihar2009_periods` in this script)

    par_ID = mated_table.Parihar2009_ID[primary_index]

    if par_ID == -1:
        return np.NaN

    # should be unique, so [0][0] is justified, unless there's no match
    try:
        par_p_index = np.where(Parihar2009_periods.Seq == par_ID)[0][0]
    except IndexError, e:
        return np.NaN

    # grab the three periods, take the median - will probs be a safe bet
    par_period = Parihar2009_periods.Per[par_p_index]

#    print par_period

    return par_period

def RL_period_get(mated_table, primary_index):
    """
    Gets a period for an input star from the Rodriguez-Ledesma 2009 table.

    Parameters
    ----------
    mated_table : atpy.Table
        Output of tablemate_script containing desired sources.
        Must have a Rodriguez-Ledesma09 index column - this implies it 
        was matched to Rodriguez-Ledesma 09 already.
    primary_index : int
        The index (starting at zero) of the input star, in the mated_table.

    Returns
    -------
    RL_period : float or np.NaN
        The Rodriguez-Ledesma 09-listed Period for the input star.
        If the star is not in the RL09 table, or does not have a listed period,
        then np.NaN is returned.

    """

    # For this function, it's a little more complicated since we have to
    # leapfrog from the Rodriguez-Ledesma table straight to the separate period table
    # (namely, Table 2: `RL2009_periods` in this script)

    RL_ID = mated_table.RL2009_ID[primary_index]

    if RL_ID == -1:
        return np.NaN

    # should be unique, so [0][0] is justified, unless there's no match
    try:
        RL_p_index = np.where(RL2009_periods.__H97b_ == RL_ID)[0][0]
    except IndexError, e:
        return np.NaN

    RL_period = RL2009_periods.Per[RL_p_index]

#    print RL_period

    return RL_period


period_funcs = [GCVS_period_get, CHS01_period_get, YSOVAR_period_get,
                Herbst_period_get, Parihar_period_get, RL_period_get]

