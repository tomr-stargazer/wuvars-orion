"""
This is a script for generating TABLES for the Orion WFCAM time-series paper.

Guide to variable names:

 =====PERIODICS======
 Currently, we're using 
 `conf_subj_periodics` for subjective periodics,
 `autovars_true_periodics` for the superset of automatically detected and pristine/strict periodic variables, and `autovars_true_periods` when we need their `best_period`s (but NEVER otherwise, for strange reasons)
 `autovars_strict_periodics` for pristine/strict variables, and `autovars_strict_periods` when we need their `best_period`s (but NEVER otherwise, for strange reasons)
 =====NON-PERIODICS======
 `conf_subj_nonpers` for subjective nonperiodics
 `autovars_true_nonpers` for the superset of automatically detected and pristine/strict nonperiodic variables
 `autovars_strict_nonpers` for pristine/strict nonperiodic variables

 =====GLOBAL======
 `autovars_true` for all automatically detected variables (incl. pristines)
 `autovars_strict` for all pristine variables
 `maxvars`

"""

# All of these imports are meant to mirror those from figure_maker.

from official_star_counter import *
from color_slope_filtering import (jhk_empty, jhk_filled, jh_empty, jh_filled,
                                   hk_empty, hk_filled)
from tablemate_comparisons import (mated_ukvar, ukvar_spread, 
                                   ukvar_periods, source_period_digger)
from tablemate_script import (Megeath2012, Megeath_P, Megeath_D)

from montage_script import conf_subj_periodics, conf_subj_nonpers


def t_table1_radec_xref_jhk_rms_minmax_irac():
    """
    Generates Table 1.

    Current columns:
      UKvar ID : int  ## note: will likely be migrated to "ONCvar ID" in paper
      RA : float, degrees
      DEC : float, degrees # note: we could probably have an optional sexg. format for these
      Median J, H, K, with error bars : six floats
      RMS J, H, K : three floats
      robust range J, H, K : three floats
      IRAC colors from Megeath, and errors : eight floats

    """

    
      
