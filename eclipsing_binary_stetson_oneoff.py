"""
This is a script that calculates the Stetson variability of eclipsing binaries
*out of eclipse*.

"""

from __future__ import division

from spread3 import Stetson_machine
import plot3
from variables_data_filterer import source_photometry

# V1916 Ori has SOURCEID: 44199508554632
v1916ori_sid = 44199508554632
v1916ori_data = source_photometry.where(source_photometry.SOURCEID == v1916ori_sid)

# Period is 1.112403 days.
v1916ori_period = 1.112403

# I looked at the lightcurve and concluded that the eclipse occurs in these phases
min_phase = 0.045
max_phase = 0.95
middle_phase_start = 0.465
middle_phase_end = 0.55

v1916ori_phase = ((v1916ori_data.MEANMJDOBS-54034) % v1916ori_period) / v1916ori_period

v1916ori_out_of_eclipse = v1916ori_data.where((v1916ori_phase > min_phase) &
	                                          (v1916ori_phase < max_phase) & 
	                                          ((v1916ori_phase < middle_phase_start) |
	                                           (v1916ori_phase > middle_phase_end)) )

print len(v1916ori_out_of_eclipse)
print "Datapoints removed: {0}".format(len(v1916ori_data) - len(v1916ori_out_of_eclipse))

print "Stetson of V1916 Ori, full data: {0}".format(Stetson_machine(v1916ori_data, flags=256))
print "Stetson of V1916 Ori out of eclipse: {0}".format(Stetson_machine(v1916ori_out_of_eclipse, flags=256))

plot3.graded_phase(v1916ori_out_of_eclipse, v1916ori_sid, period=v1916ori_period, timecolor=True,
	               name="V1916 Ori, eclipse data removed")

plot3.graded_phase(v1916ori_data, v1916ori_sid, period=v1916ori_period, timecolor=True,
	               name="V1916 Ori, with eclipses")
