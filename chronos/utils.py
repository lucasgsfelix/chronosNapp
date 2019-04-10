#pylint: disable=mixed-indentation
"""Utility features for all backends"""
from datetime import datetime

class Utils:
	"""Utility methods for the backends"""
	def validate_timestamp(self, start_timestamp, end_timestamp):
		"""Method use for validate the time stamp,
		avoiding that end_timestamp be smaller than start_timestamp"""
		start_timestamp = datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S").timestamp()
		end_timestamp = datetime.strptime(end_timestamp, "%Y-%m-%d %H:%M:%S").timestamp()
		if start_timestamp > end_timestamp:
			assert "Invalid Data Range !"
