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

Carpenter2001_periods = atpy.Table(dpath+"Carpenter2001_datafile7.txt")

def GCVS_period_get():
    """ Gets a period for an input star from the GCVS table."""
    pass

def CHS01_period_get():
    """ Gets a period for an input star from the Carpenter 2001 table."""
    pass

def YSOVAR_period_get():
    """ Gets a period for an input star from the YSOVAR Orion table."""
    pass

def Herbst_period_get():
    """ Gets a period for an input star from the Herbst 2002 table."""
    pass

def Parihar_period_get():
    """ Gets a period for an input star from the Parihar 2009 table."""
    pass

