"""
Extensions to wuvars-proto/tr/plot4.py that are relevant to Orion.

"""

from __future__ import division

from plot4 import StarData

class OrionStarData(StarData):
	def __init__(self, table, sid):
		StarData.__init__(self, table, sid, date_offset=54034)

