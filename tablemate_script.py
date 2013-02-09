"""
This is the SCRIPT that mates tables in the Orion catalog,
by calling the MODULE orion_tablemate.py.

"""



import orion_tablemate
from orion_tablemate import TableParameters, atpy

# Top half of the script: defining various tables

dpath = "/home/tom/Dropbox/Bo_Tom/aux_catalogs/"

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

DaRio_2009 = TableParameters(
    data = dpath+"DaRio2009_table2.fits",
    alias = "DaRio2009",
    full_name = "'Table 2: WFI Photometric Catalog Relative to Night A Observations', from 'A Multi-Color Optical Survey of the Orion Nebula Cluster. I. The Catalog' by Da Rio et al., 2009",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = '__DRS2009_')

DaRio_2010 = TableParameters(
    data = dpath+"DaRio2010_table3.fits",
    alias = "DaRio2010",
    full_name = "'Table 3: Positions in the HRD and Values of Mass and Age from Siess et al. (2000) and Palla & Stahler (1999)' from 'A Multi-Color Optical Survey of the Orion Nebula Cluster. II. The H-R Diagram' by Da Rio et al., 2010",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = 'ID')

YSOVAR_YSOs = TableParameters(
    data = atpy.Table(dpath+"YSOVAR_OrionYSOs.table", type='ascii'),
    alias = "YSOVAR_OrionYSOs",
    full_name = "'Table for the 1396 ONC Stars with IR Excesses', from 'YSOVAR: The First Sensitive, Wide-Area, Mid-Infrared Photometric Monitoring of the Orion Nebula Cluster' by Morales-Calderon et al., 2011",
    ra_cols = ['RA_IRAC'], dec_cols = ['DEC_IRAC'],
    radec_fmt = 'decimal degrees',
    name_col = 'SOYname')

YSOVAR_NoExcess = TableParameters(
    data = atpy.Table(dpath+"YSOVAR_OrionNoExcess.table", type='ascii'),
    alias = "YSOVAR_OrionNoExcess",
    full_name = "'Table for the 1027 ONC candidate members not known to have IR Excesses', from 'YSOVAR: The First Sensitive, Wide-Area, Mid-Infrared Photometric Monitoring of the Orion Nebula Cluster' by Morales-Calderon et al., 2011",
    ra_cols = ['RA_IRAC'], dec_cols = ['DEC_IRAC'],
    radec_fmt = 'decimal degrees',
    name_col = 'SOYname')

Herbst2002 = TableParameters(
    data = dpath+"Herbst2002_table1.fits",
    alias = "Herbst2002",
    full_name = "'Photometric data', from 'Stellar Rotation and Variability in the Orion Nebula Cluster' by Herbst et al. 2002",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = 'ID')


COUP_Getman2005 = TableParameters(
    data = atpy.Table(dpath+"COUP_Getman2005_datafile2.txt", type='ascii'),
    alias = "COUP_Getman2005",
    full_name = "'Table 2: COUP X-Ray Source Locations', from 'Chandra Orion Ultradeep Project: Observations and Source Lists' by Getman et al., 2005",
    ra_cols = ['RAdeg'], dec_cols = ['DEdeg'],
    radec_fmt = 'decimal degrees',
    name_col = 'CXOONCJ')

Parihar2009 = TableParameters(
    data = dpath+"Parihar2009_table2.fits",
    alias = "Parihar2009",
    full_name = "'Table 2: The photometric data along with other relevant information of all 346 stars in our FOV.', from 'Exploring pre-main-sequence variables of the ONC: the new variables' by Parihar et al., 2009.",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal degrees',
    name_col = 'Seq')

Robberto2010 = TableParameters(
    data = dpath+"Robberto2010_table5.fits",
    alias = "Robberto2010",
    full_name = "'Table 5: ISPI Photometry and Astrometry of the ONC', from 'A Wide-Field Survey of the Orion Nebula Cluster in the Near-Infrared' by Robberto et al., 2010.",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'ID')

eso_ha = TableParameters(
    data = dpath+"ESOHa_m42_fc_P_fits.fits", 
    alias = "ESO_Ha_PAR",
    full_name = "'ESO H-alpha survey of ONC, 5 x 5 degrees' by Petterson, B.; Armond, T.; & Reipurth, B. 2013, in prep.",
    ra_cols = ['R.A.(2000)', 'col7', 'col8'], 
    dec_cols = ['Dec(2000)', 'col10', 'col11'],
    radec_fmt = 'sex-three',
    name_col = '2MASS identity')


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
            
