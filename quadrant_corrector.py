"""
This is a Python module to correct 'bad' nights in the 
UKIRT Orion data, and perhaps other similar datasets.
It relies on the principle of finding nearby constant stars
to use for reference magnitudes on every night.

In particular, each star is compared to four reference stars, 
one located in each quadrant (NE, SE, SW, NW) for ease of computation
and to ensure that they enclose the given star.

"""

def quadrant_corrector(data, constant_list, band):
    """
    Corrects magnitudes using a network of constant stars.

    Parameters
