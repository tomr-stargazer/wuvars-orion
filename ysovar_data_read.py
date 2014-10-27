"""
This is a short script that reads in the YSOVAR orion data for ONCvar 1226.

"""

from __future__ import division

import os.path

import matplotlib.pyplot as plt

import astropy.table


data_path = os.path.expanduser("~/Dropbox/Bo_Tom/ysovar/")

yso = astropy.table.Table.read(data_path+'YSOVAR9825.csv')

irac1 = yso['filter'] == 4
irac2 = yso['filter'] == 5

def make_ysovar_light_curve():

    fig = plt.figure(figsize=(7,4))

    plt.errorbar(yso['mjd'][irac1]-54034, yso['mag1'][irac1], yerr=yso['emag1'][irac1], fmt='ms', ms=4)
    plt.errorbar(yso['mjd'][irac2]-54034, yso['mag1'][irac2], yerr=yso['emag1'][irac2], fmt='ko', ms=4)

    plt.text(1127, 10.73, "IRAC1 [3.6]", fontsize=16)
    plt.text(1128, 10.9, "IRAC2 [4.5]", fontsize=16, color='m')

    plt.xlim(1090,1140)
    plt.ylim(11.05,10.35)
    plt.xlabel("Time (MJD - 54034)")
    plt.ylabel("Magnitude")

    return fig