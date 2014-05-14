"""
Extensions to wuvars-proto/tr/plot4.py that are relevant to Orion.

"""

from __future__ import division

from plot4 import StarData
from orion_abridger import abridger as orion_abridger

class OrionStarData(StarData):
	def __init__(self, table, sid, name=None):
		StarData.__init__(self, table, sid, name=name, date_offset=54034, abridger=orion_abridger)

