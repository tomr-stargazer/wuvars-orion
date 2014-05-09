"""
A script to figure out whether the distribution of color slopes
is a function of how long you observe or how many times you observe.

Incidentally, this kind of thing might also be a good strategy for 
discovering or selecting variables who change their variability mechanism 
in our observations. (currently, we're scanning by eye).

This could ALSO be used to plot typical variability amplitudes versus 
time baseline, especially as a function of variable class.

"""

from __future__ import division
import random
from functools import partial

import numpy as np
import atpy

import spread3

from table_maker import make_megeath_class_column
from variables_data_filterer import variables_photometry, autovars_true, ukvar_spread
from color_slope_filtering import filter_color_slopes
from robust import mad

megeath_class_column = make_megeath_class_column()

protostar_IDs = ukvar_spread.SOURCEID[megeath_class_column == 'P']
disk_IDs = ukvar_spread.SOURCEID[megeath_class_column == 'D']
nondisk_IDs = ukvar_spread.SOURCEID[megeath_class_column == 'ND']

def compute_function_on_column(function, column, spreadsheet):
    return function(spreadsheet[column])

def compute_function_on_column_selected(function, column, selection, spreadsheet):
    return function(spreadsheet[column][np.in1d(spreadsheet.SOURCEID, selection)])

def get_timespan(data): 
    return (data.MEANMJDOBS.max() - data.MEANMJDOBS.min())

def get_n_variables_stetson(spreadsheet, stetson=1.0):
    return len(spreadsheet[spreadsheet.Stetson >= stetson])

def get_n_obs(data):
    return len(list(set(np.floor(data.MEANMJDOBS))))


def calculate_color_slope_ratios_versus_time_baseline(delta_t_list=None, date_offset=0, shuffle_dates=False):
    """
    Calculates the color slope ratios for each possible time baseline.

    """

    autovars_photometry = variables_photometry.where(
        np.in1d(variables_photometry.SOURCEID, autovars_true.SOURCEID) & 
        (variables_photometry.MEANMJDOBS >= np.min(variables_photometry.MEANMJDOBS) + date_offset))

    date_list = np.sort(list(set(np.floor(autovars_photometry.MEANMJDOBS))))

    # I think this is the only place I need to shuffle? Maybe?
    if shuffle_dates:
        random.shuffle(autovars_photometry.MEANMJDOBS)

    n_positive_slope_list = []
    n_negative_slope_list = []
    n_undef_slope_list = []

    n_variables_list = []

    # calculate these properties:
    # most basic
    properties = [{'name':'time_baseline',
                   'function':get_timespan,
                   'target':'data',
                   'container':[]},

                   {'name':'n_obs',
                   'function':get_n_obs,
                   'target':'data',
                   'container':[]}]

    # how many variables, using different stetson cuts?
    properties.extend(
        [{'name':'n_variables_{0}'.format(x),
          'function':partial(get_n_variables_stetson, stetson=x),
          'target':'spreadsheet',
          'container':[]} 
          for x in (0.8, 1.0, 1.2) ] )

    # basic properties -- j, h, k amplitudes / deviations
    properties.extend(
       [{'name':'median_{0}_{1}'.format(x,y1),
         'function':partial(compute_function_on_column,y2,'{0}_ranger'.format(x)),
         'target':'spreadsheet',
         'container':[]
         } 
         for x in ('j', 'h', 'k')
         for y1, y2 in zip(('amplitude', 'deviation'), (np.median, mad))] )

    # now broken down into Class
    properties.extend(
       [{'name':'{2}_median_{0}_{1}'.format(x,y1, z1),
         'function':partial(compute_function_on_column_selected,y2,'{0}_ranger'.format(x),z2),
         'target':'spreadsheet',
         'container':[]
         } 
         for x in ('j', 'h', 'k')
         for y1, y2 in zip(('amplitude', 'deviation'), (np.median, mad))
         for z1, z2 in zip(('protostar', 'disk', 'nondisk'), (protostar_IDs, disk_IDs, nondisk_IDs))] )


    # For a bunch of different obs_initial's...
    # (note: when we test this, we may want to only go from the FIRST observation, and then add in the complexity of all the other ones later)
    # also note: we'll probably want to truncate the MJDs to the nearest integer to avoid any complications from the whole four-exposures-per-band-per-night thing.
    last_n_obs = 0
    for obs_initial in date_list:

        print "Starting from: MJD %f" % obs_initial
        longest_time_separation = max(date_list) - obs_initial

        if delta_t_list == None:
            delta_t_list = range(int(np.ceil(longest_time_separation)))

        for delta_t in delta_t_list:

            relevant_data = autovars_photometry.where(
                (autovars_photometry.MEANMJDOBS >= obs_initial) &
                (autovars_photometry.MEANMJDOBS < obs_initial + delta_t) )

            n_obs = len(list(set(np.floor(relevant_data.MEANMJDOBS))))
            print "%d observations over %d (delta-t) days" % (n_obs, delta_t)

            if n_obs < 2:
                print "not enough observations for this to be called 'variability'. Continuing."
                continue
            elif n_obs == last_n_obs:
                print "No new observations have been added. Continuing."
                continue
            else:
                last_n_obs = n_obs

            # note: 
            # if you don't add any new observations between this delta-t 
            # and the last delta-t, DON'T COMPUTE A SPREADSHEET. just continue.  
            # if timespan_of_relevant_data <= (delta_t - 1):
            #     print timespan_of_relevant_data, delta_t, "timespan is too short to be considered in this delta_t bin. Continuing."
            #                continue

            relevant_lookup = spread3.base_lookup(relevant_data, 0 )
            relevant_spreadsheet = spread3.spreadsheet_write_efficient(
                20, relevant_data, relevant_lookup, -1, None,
                flags=0, colorslope=True, rob=True)

            # then run color_slope_filtering on it...
            relevant_khk_spreadsheet = filter_color_slopes(
                relevant_spreadsheet, 'hk', 
                lower_obs_limit=n_obs/3, upper_obs_limit=n_obs*1.5)
            relevant_khk_spreadsheet_no_slope_confidence = filter_color_slopes(
                relevant_spreadsheet, 'hk', slope_confidence=None,
                lower_obs_limit=n_obs/3, upper_obs_limit=n_obs*1.5)

            targets = {}
            targets['spreadsheet'] = relevant_spreadsheet
            targets['data'] = relevant_data

            # and extract which guys have colors in the relevant ranges!
            n_positive_slope = len(relevant_khk_spreadsheet[
                (np.degrees(np.arctan(relevant_khk_spreadsheet.khk_slope)) > 25) ])
            n_negative_slope = len(relevant_khk_spreadsheet[
                (np.degrees(np.arctan(relevant_khk_spreadsheet.khk_slope)) < -25) ])
            n_undef_slope = (len(relevant_khk_spreadsheet_no_slope_confidence) -
                                (n_positive_slope + n_negative_slope) )

            n_variables = len(relevant_spreadsheet[relevant_spreadsheet.Stetson >= 1.0])

            for prop in properties:
                prop['container'].append(prop['function'](targets[prop['target']]) )

            n_positive_slope_list.append( n_positive_slope )
            n_negative_slope_list.append( n_negative_slope )
            n_undef_slope_list.append( n_undef_slope )

            n_variables_list.append( n_variables)

        break

    color_slope_ratios_table = atpy.Table()

    addc = color_slope_ratios_table.add_column

    addc("n_positive_slope", n_positive_slope_list)
    addc("n_negative_slope", n_negative_slope_list)
    addc("n_undef_slope", n_undef_slope_list)

    addc("n_variables", n_variables_list)

    for prop in properties:
        addc(prop['name'], prop['container'])

    return color_slope_ratios_table



def plot_color_slope_ratios_versus_time_baseline():
    """
    Plot color slope ratios versus time baseline.

    Also consider plotting "number of stars with significant color variability"
    versus time baseline.

    This will intrinsically be a scatterplot.
    Points with more observations in them may deserve bigger dots or something.

    """
    
    pass
