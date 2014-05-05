"""
This is a script that calculates the Stetson variability of eclipsing binaries
*out of eclipse*.

"""

from __future__ import division

from variables_data_filterer import source_photometry

# V1916 Ori has SOURCEID: 44199508554632
v1916ori_data = source_photometry.where(source_photometry.SOURCEID == 44199508554632)

# Period is 1.112403 days.
v1916ori_period = 1.112403

# I looked at the lightcurve and concluded that the eclipse 
