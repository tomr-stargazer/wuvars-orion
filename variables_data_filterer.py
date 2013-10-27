"""
Removes all stars from our source data except "final" variables.

"""

from __future__ import division
import os

import numpy as np

import atpy

from tablemate_comparisons import ukvar_spread
from official_star_counter import maxvars, autovars_true

dropbox_bo_data = os.path.expanduser("~/Dropbox/Bo_Tom/data/")

source_photometry = atpy.Table(
    dropbox_bo_data + "fdece_graded_clipped0.8_scrubbed0.1_dusted0.5.fits")

variables_photometry = source_photometry.where(
    np.in1d(source_photometry.SOURCEID, ukvar_spread.SOURCEID))

def filter_by_tile():
    """
    Splits the input data tables into 16 tiles, avoiding overlap regions.

    Uses the spatial extent of the `maxvars` spreadsheet to figure out
    where the bounds of the tiles are.

    Only returns data pertaining to our 1202 variables.

    Returns
    -------
    tile_tables : list of atpy.Table
        A list of the variable star photometry tables 
        corresponding to each tile.
    tile_spreadsheets : list of atpy.Table
        A list of the variable star variability spreadsheets
        corresponding to each table.
        
    """

    vp = variables_photometry

    max_ra = maxvars.RA.max()
    min_ra = maxvars.RA.min()
    max_dec = maxvars.DEC.max()
    min_dec = maxvars.DEC.min()

    tile_size_ra = (max_ra - min_ra) / 4
    tile_size_dec = (max_dec - min_dec) / 4

    tile_tables = []
    tile_spreadsheets = []
    
    for ra_i in range(4):

        for dec_j in range(4):

            tile_min_ra = min_ra + tile_size_ra*ra_i + tile_size_ra/10
            tile_max_ra = min_ra + tile_size_ra*(ra_i+1) - tile_size_ra/10

            tile_min_dec = min_dec + tile_size_dec*dec_j + tile_size_dec/10
            tile_max_dec = min_dec + tile_size_dec*(dec_j+1) - tile_size_dec/10

            tile_photometry = vp.where(
                (vp.RA > tile_min_ra) & (vp.RA < tile_max_ra) &
                (vp.DEC > tile_min_dec) & (vp.DEC < tile_max_dec) )

            tile_spreadsheet = ukvar_spread.where(
                (ukvar_spread.RA > tile_min_ra) & 
                (ukvar_spread.RA < tile_max_ra) &
                (ukvar_spread.DEC > tile_min_dec) & 
                (ukvar_spread.DEC < tile_max_dec) )

            tile_tables.append(tile_photometry)
            tile_spreadsheets.append(tile_spreadsheet)

    return tile_tables, tile_spreadsheets

def check_max_observations_per_tile():

    tile_tables, tile_spreadsheets = filter_by_tile()

    for i, tile_spreadsheet in zip(range(len(tile_spreadsheets)), 
                                   tile_spreadsheets):

        ts = tile_spreadsheet
        
        print ("Tile %d, N_J: %3d, N_H: %3d, N_K: %3d" % 
               (i, ts.N_j.max(), ts.N_h.max(), ts.N_k.max()))
