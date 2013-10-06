"""
This is the SCRIPT that mates tables in the Orion catalog,
by calling the MODULE orion_tablemate.py.

This should be kept, broadly, in sync with the Google Doc
"Auxiliary Tables in ONC".

We are asking three broad questions:
1. How many of our variables are previously-known sources?
2. How many of our variables are previously-known variables?
3. How many previously-known variables in this field do we recover?

"""

import os

import numpy as np

import orion_tablemate
from orion_tablemate import TableParameters, atpy
import megeath_fulltable_parser_oneoff

# Top half of the script: defining various tables

dpath = os.path.expanduser("~/Dropbox/Bo_Tom/aux_catalogs/")
tables = []


Rice_2013_vars = TableParameters(
    data = dpath+"gluedvars_1240_variables.fits",
    alias= "Rice2013_vars",
    full_name = "'Master spreadsheet for 1240 variables', from 'High-amplitude and Periodic Near-Infrared Variables in the Orion Nebula Cluster', Rice, Reipurth, Vaz, Wolk, Cross, Guimaraes 2013.",
    ra_cols = ['RA'], dec_cols=['DEC'],
    radec_fmt = 'decimal-radians',
    name_col = 'SOURCEID')

Rice_UKvars =  TableParameters(
    data = dpath+"UKvar_spreadsheet_withSIMBADnames_w1226_minusEasties.fits",
    alias= "Rice2013_UKvars",
    full_name = "'Master spreadsheet for 1202 ONC variables', from 'High-amplitude and Periodic Near-Infrared Variables in the Orion Nebula Cluster', Rice, Reipurth, Vaz, Wolk, Cross, Guimaraes 2013.",
    ra_cols = ['RA'], dec_cols=['DEC'],
    radec_fmt = 'decimal-radians',
    name_col = 'UKvar_ID')


Rice_2013_all = TableParameters(
    data = dpath+"Rice_allsources_spreadsheet_2013_02_13.fits",
    alias= "Rice2013_all",
    full_name = "'Master spreadsheet for all 40630 detected sources', from 'High-amplitude and Periodic Near-Infrared Variables in the Orion Nebula Cluster', Rice, Reipurth, Vaz, Wolk, Cross, Guimaraes 2013.",
    ra_cols = ['RA'], dec_cols=['DEC'],
    radec_fmt = 'decimal-radians',
    name_col = 'SOURCEID')

Twomass = TableParameters(
    data = dpath+"fp_2mass.fp_psc27078_M42_boxdegree_search.tbl",
    alias = "2MASS_PSC",
    full_name = "Two Micron All-Sky Survey: All-Sky Data Release Point Source Catalog. Released 2003 Mar 25. Box search: center (83.83743,-5.41019), sidelength 3600 arcsec.",
    ra_cols = ['ra'], dec_cols = ['dec'],
    radec_fmt = 'decimal-degrees',
    name_col = 'designation')
tables.append(Twomass)

Wise = TableParameters(
    data = dpath+"wise_allsky.wise_allsky_4band_M42_boxdegree_search.tbl",
    alias = "WISE",
    full_name = "Wide-field Infrared Survey Explorer (WISE) All-Sky Source Catalog. Box search: center (83.83743,-5.41019), sidelength 3800.02 arcsec.",
    ra_cols = ['ra'], dec_cols = ['dec'],
    radec_fmt = 'decimal-degrees',
    name_col = 'designation')
tables.append(Wise)

GCVS = TableParameters(
    data = dpath+"GCVS_version2012_Orion_selection.fits",
    alias = "GCVS",
    full_name = "General Catalogue of Variable Stars, version 2012-04-15",
    ra_cols = ["RAJ2000"], dec_cols = ["DEJ2000"],
    radec_fmt = 'decimal degrees',
    name_col = 'GCVS')
tables.append(GCVS)
    

Carpenter_2001 = TableParameters(
    # data
    data = dpath+"Carpenter2001_table4.fits",
    # alias
    alias = "CHS2001",
    # full_name
    full_name = "Table 4. 'Near-Infrared Variable Stars', from 'Near-Infrared Photometric Variability of Stars Toward the Orion A Molecular Cloud' by Carpenter, John M.; Hillenbrand, Lynne A.; Skrutskie, M. F. 2001AJ....121.3160C",
    # ra_cols, dec_cols
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    #radec_fmt
    radec_fmt = 'decimal degrees',
    #name_col
    name_col = '__CHS2001_')
tables.append(Carpenter_2001)

DaRio_2009 = TableParameters(
    data = dpath+"DaRio2009_table2.fits",
    alias = "DaRio2009",
    full_name = "'Table 2: WFI Photometric Catalog Relative to Night A Observations', from 'A Multi-Color Optical Survey of the Orion Nebula Cluster. I. The Catalog' by Da Rio et al., 2009",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = '__DRS2009_')
tables.append(DaRio_2009)

DaRio_2010 = TableParameters(
    data = dpath+"DaRio2010_table3.fits",
    alias = "DaRio2010",
    full_name = "'Table 3: Positions in the HRD and Values of Mass and Age from Siess et al. (2000) and Palla & Stahler (1999)' from 'A Multi-Color Optical Survey of the Orion Nebula Cluster. II. The H-R Diagram' by Da Rio et al., 2010",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = 'ID')
tables.append(DaRio_2010)

YSOVAR_YSOs = TableParameters(
    data = atpy.Table(dpath+"YSOVAR_OrionYSOs.table", type='ascii'),
    alias = "YSOVAR_OrionYSOs",
    full_name = "'Table for the 1396 ONC Stars with IR Excesses', from 'YSOVAR: The First Sensitive, Wide-Area, Mid-Infrared Photometric Monitoring of the Orion Nebula Cluster' by Morales-Calderon et al., 2011",
    ra_cols = ['RA_IRAC'], dec_cols = ['DEC_IRAC'],
    radec_fmt = 'decimal degrees',
    name_col = 'SOYname')
tables.append(YSOVAR_YSOs)

YSOVAR_NoExcess = TableParameters(
    data = atpy.Table(dpath+"YSOVAR_OrionNoExcess.table", type='ascii'),
    alias = "YSOVAR_OrionNoExcess",
    full_name = "'Table for the 1027 ONC candidate members not known to have IR Excesses', from 'YSOVAR: The First Sensitive, Wide-Area, Mid-Infrared Photometric Monitoring of the Orion Nebula Cluster' by Morales-Calderon et al., 2011",
    ra_cols = ['RA_IRAC'], dec_cols = ['DEC_IRAC'],
    radec_fmt = 'decimal degrees',
    name_col = 'SOYname')
tables.append(YSOVAR_NoExcess)

Herbst2002 = TableParameters(
    data = dpath+"Herbst2002_table1.fits",
    alias = "Herbst2002",
    full_name = "'Photometric data', from 'Stellar Rotation and Variability in the Orion Nebula Cluster' by Herbst et al. 2002",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = 'ID')
tables.append(Herbst2002)


COUP_Getman2005 = TableParameters(
    data = atpy.Table(dpath+"COUP_Getman2005_datafile2.txt", type='ascii'),
    alias = "COUP_Getman2005",
    full_name = "'Table 2: COUP X-Ray Source Locations', from 'Chandra Orion Ultradeep Project: Observations and Source Lists' by Getman et al., 2005",
    ra_cols = ['RAdeg'], dec_cols = ['DEdeg'],
    radec_fmt = 'decimal degrees',
    name_col = 'CXOONCJ')
tables.append(COUP_Getman2005)

Parihar2009 = TableParameters(
    data = dpath+"Parihar2009_table2.fits",
    alias = "Parihar2009",
    full_name = "'Table 2: The photometric data along with other relevant information of all 346 stars in our FOV.', from 'Exploring pre-main-sequence variables of the ONC: the new variables' by Parihar et al., 2009.",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = 'Seq')
tables.append(Parihar2009)

Robberto2010 = TableParameters(
    data = dpath+"Robberto2010_table5.fits",
    alias = "Robberto2010",
    full_name = "'Table 5: ISPI Photometry and Astrometry of the ONC', from 'A Wide-Field Survey of the Orion Nebula Cluster in the Near-Infrared' by Robberto et al., 2010.",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'ID')
tables.append(Robberto2010)

DaRio2012 = TableParameters(
    data = atpy.Table(dpath+"DaRio2012_table3.txt", type='ascii'),
    alias = "DaRio2012",
    full_name = "'Table 3: Derived Stellar Parameters of the ONC Population', from 'The Initial Mass Function of the Orion Nebula Cluster Across the H-Burning Limit' by Da Rio et al. 2012.",
    ra_cols = ['RAh', 'RAm', 'RAs'], 
    dec_cols = ['DE-', 'DEd', 'DEm', 'DEs'],
    radec_fmt = 'sex-three-four',
    name_col = 'ID')
tables.append(DaRio2012)

Manara2012_table2 = TableParameters(
    data = atpy.Table(dpath+"Manara2012_table2.txt", type='ascii'),
    alias="Manara2012_table2",
    full_name= "'Table 2: Stellar parameters of the sources where the 2CD method leads to a determination of A_V and L_acc', from 'HST Measures of Mass Accretion Rates in the Orion Nebula Cluster', by Manara et al. 2012. 2012ApJ...755..154M",
    ra_cols = ['RAh', 'RAm', 'RAs'],
    dec_cols = ['DE-', 'DEd', 'DEm', 'DEs'],
    radec_fmt = 'sex-three-four',
    name_col = 'OM')
tables.append(Manara2012_table2)

Andersen2011 = TableParameters(
    data = dpath+"Andersen2011_table1.fits",
    alias = "Andersen2011",
    full_name = "'Table 1: Sources detected in the NICMOS camera 3 mosaics', from 'The low-mass initial mass function in the Orion nebula cluster based on HST/NICMOS III imaging' by Andersen et al. 2011. 2011A&A...534A..10A",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = 'Seq')
tables.append(Andersen2011)
    

eso_ha = TableParameters(
    data = dpath+"ESOHa_m42_fc_P_fits.fits", 
    alias = "ESO_Ha_PAR",
    full_name = "'ESO H-alpha survey of ONC, 5 x 5 degrees' by Petterson, B.; Armond, T.; & Reipurth, B. 2013, in prep.",
    ra_cols = ['R.A.(2000)', 'col7', 'col8'], 
    dec_cols = ['Dec(2000)', 'col10', 'col11'],
    radec_fmt = 'sex-three',
    name_col = '2MASS identity')
tables.append(eso_ha)

Megeath2012 = TableParameters(
    data = atpy.Table(dpath+"Megeath2012_table1.txt", type='ascii'),
    alias = "Megeath2012",
    full_name = "'Table 1: Spitzer-identified YSOs: IRAC, MIPS, and 2MASS Magnitudes', from 'The Spitzer Space Telescope Survey of the Orion A & B Molecular Clouds - Part I: A Census of Dusty Young Stellar Objects and a Study of their Mid-IR Variability' by Megeath et al., 2012.",
    ra_cols = ["RAh", "RAm", "RAs"],
    dec_cols = ["DE-", "DEd", "DEm", "DEs"],
    radec_fmt = 'sex-three-four',
    name_col = 'Num')
tables.append(Megeath2012)

Stassun1999 = TableParameters(
    data = dpath+"Stassun1999_table1.fits",
    alias = "Stassun1999",
    full_name = "'Table 1: Data for Rotator Sample', from 'The Rotation Period Distribution of Pre-Main-Sequence Stars in and around the Orion Nebula' by Stassun et al., 1999.",
    ra_cols = ['RAJ2000'],
    dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = '__SMM99_')
#tables.append(Stassun1999)

RodriguezLedesma2009 = TableParameters(
    data = dpath+"RodriguezLedesma2009_table1.fits",
    alias = "RL2009",
    full_name = "'Table 1: Sample of the photometric catalogue,' from 'Rotational studies in the Orion Nebula Cluster: from solar mass stars to brown dwarfs' by Rodriguez-Ledesma et al., 2009. 2009A&A...502..883R",
    ra_cols = ['RAJ2000'],
    dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = '__H97b_')
tables.append(RodriguezLedesma2009)

xmm_north_data = atpy.Table(dpath+"matches_xmm_spitzer_north2.txt", 
                            type='ascii')
xmm_north_data.add_column('Index', np.arange(len(xmm_north_data)))

XMM_north = TableParameters(
    data = xmm_north_data,
    alias = "XMMnorth",
    full_name = "Mysterious XMM north table from Ignazio",
    ra_cols = ['ra'],
    dec_cols = ['dec'],
    radec_fmt = 'decimal degrees',
    name_col = 'Index')

# Just the class one sources
XMM_north_c1 = TableParameters(
    data = xmm_north_data.where(xmm_north_data.proto == 1),
    alias = "XMMnorth_c1",
    full_name = "XMM north table: Class I ('proto')",
    ra_cols = ['ra'],
    dec_cols = ['dec'],
    radec_fmt = 'decimal degrees',
    name_col = 'Index')

# Just the class two sources
XMM_north_c2 = TableParameters(
    data = xmm_north_data.where(xmm_north_data.disks ==1),
    alias = "XMMnorth_c2",
    full_name = "XMM north table: Class II ('disks')",
    ra_cols = ['ra'],
    dec_cols = ['dec'],
    radec_fmt = 'decimal degrees',
    name_col = 'Index')

# Just the class three sources
XMM_north_c3 = TableParameters(
    data = xmm_north_data.where(xmm_north_data.c3cnd =="1"),
    alias = "XMMnorth_c3",
    full_name = "XMM north table: Class III ('c3cnd')",
    ra_cols = ['ra'],
    dec_cols = ['dec'],
    radec_fmt = 'decimal degrees',
    name_col = 'Index')

Megeath_P = TableParameters(
    data = (Megeath2012.data.
            where(Megeath2012.data.Class == 'P') ),
    alias = "Megeath2012_P",
    full_name = "Protostar ('P' only) Selection from 'Table 1: Spitzer-identified YSOs: IRAC, MIPS, and 2MASS Magnitudes', from 'The Spitzer Space Telescope Survey of the Orion A & B Molecular Clouds - Part I: A Census of Dusty Young Stellar Objects and a Study of their Mid-IR Variability' by Megeath et al., 2012.",
    ra_cols = ["RAh", "RAm", "RAs"],
    dec_cols = ["DE-", "DEd", "DEm", "DEs"],
    radec_fmt = 'sex-three-four',
    name_col = 'Num')

Megeath_D = TableParameters(
    data = (Megeath2012.data.
            where(Megeath2012.data.Class == 'D')),
    alias = "Megeath2012_D",
    full_name = "Disk Selection from 'Table 1: Spitzer-identified YSOs: IRAC, MIPS, and 2MASS Magnitudes', from 'The Spitzer Space Telescope Survey of the Orion A & B Molecular Clouds - Part I: A Census of Dusty Young Stellar Objects and a Study of their Mid-IR Variability' by Megeath et al., 2012.",
    ra_cols = ["RAh", "RAm", "RAs"],
    dec_cols = ["DE-", "DEd", "DEm", "DEs"],
    radec_fmt = 'sex-three-four',
    name_col = 'Num')

Megeath_Full = TableParameters(
    data = megeath_fulltable_parser_oneoff.get_full_megeath_table(truncated=True),
    alias = "Megeath2012_Full",
    full_name = "'the entire Spitzer Orion Survey Point Source Catalog', from http://astro1.physics.utoledo.edu/~megeath/Orion/The_Spitzer_Orion_Survey.html",
    ra_cols = ['RA'], dec_cols=['Dec'],
    radec_fmt = 'decimal-degrees',
    name_col = 'IDL_index')
tables.append(Megeath_Full)

Megeath_Allgoodsources = TableParameters(
    data = megeath_fulltable_parser_oneoff.get_full_megeath_table(
        truncated=True, all=True),
    alias = "Megeath2012_Allgoodsources",
    full_name = "'Good-quality sources from Spitzer Orion Survey Point Source Catalog', from http://astro1.physics.utoledo.edu/~megeath/Orion/The_Spitzer_Orion_Survey.html",
    ra_cols = ['RA'], dec_cols=['Dec'],
    radec_fmt = 'decimal-degrees',
    name_col = 'IDL_index')
tables.append(Megeath_Allgoodsources)

    
# Here's our first function, that we'll use just to get things rolling
def test():
    wov = orion_tablemate.osc.autovars_strict

    wov_avs = TableParameters(
        #data
        wov,
        #alias
        "WFCAM Orion",
        #full name
        "Strict automatic variables found in the WFCAM Orion monitoring survey. From 'High Amplitude and Periodic Near-Infrared Variables in the Orion Nebula Cluster' by Rice, Thomas S.; Reipurth, Bo; et al.",
        #ra_cols, dec_cols
        ['RA'], ['DEC'],
        #radec_fmt
        'decimal radians',
        #name_col
        'SOURCEID')


    return orion_tablemate.tablemater(wov_avs, [
            Herbst2002, YSOVAR_NoExcess, YSOVAR_YSOs, DaRio_2010,
            DaRio_2009, Carpenter_2001, COUP_Getman2005, eso_ha])
            


def vars_match():
    """ 
    A function that matches our variables table to all the other tables!

    Takes about 15 seconds (2/13/13).
    """

    return orion_tablemate.tablemater( Rice_2013_vars, tables)

def UKvars_match():
    
    return orion_tablemate.tablemater( Rice_UKvars, tables)
