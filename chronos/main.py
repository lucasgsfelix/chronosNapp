#pylint: disable=mixed-indentation
"""Main module of kytos/Cronos Kytos Network Application.

Napp to store itens along time
"""
from datetime import datetime
from backends.influx import InfluxBackend
from backends.csvbackend import CSVBackend
from backends.rrd import RRDBackend
#from backends.rrd import RrdBackend

from kytos.core import KytosNApp, log
#from napps.kytos.Cronos import settings

import settings
import os

def treat_timestamp(timestamp):
	"""Treat timestamp to avoid break the searchs and insertions"""
	if not timestamp is None:
		if isinstance(timestamp, str):
			timestamp = int(timestamp)
		timestamp = datetime.utcfromtimestamp(timestamp)
		timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
	return timestamp

class Main(KytosNApp):
	"""Main class of kytos/Cronos NApp.

	This class is the entry point for this napp.
	"""
	backend = None

	def setup(self):
		"""Init method for the napp."""
		log.info("Time Series NApp started.")

		if settings.DEFAULT_BACKEND == 'INFLUXDB':
			self.backend = InfluxBackend()
		elif settings.DEFAULT_BACKEND == 'RRD':
			self.backend = RRDBackend()
		elif settings.DEFAULT_BACKEND == 'CSV':
			self.backend = CSVBackend()

	def save(self, namespace, value, timestamp=None):
		"""Save the data in one of the backends."""
		timestamp = treat_timestamp(timestamp)
		self.backend.save(namespace, value, timestamp)

	def delete(self, namespace, start_timestamp, end_timestamp, file_name=None):
		"""Delete the data in one of the backends."""
		start_timestamp = treat_timestamp(start_timestamp)
		end_timestamp = treat_timestamp(end_timestamp)
		if settings.DEFAULT_BACKEND == 'CSV':
			self.backend.delete(file_name, start_timestamp, end_timestamp)
		else:
			self.backend.delete(namespace, start_timestamp, end_timestamp)

	def get(self, namespace, start_timestamp=None, end_timestamp=None, file_name=None):
		"""Retrieve the data from one of the backends."""
		start_timestamp = treat_timestamp(start_timestamp)
		end_timestamp = treat_timestamp(end_timestamp)
		if settings.DEFAULT_BACKEND == 'CSV':
			self.backend.get(file_name, start_timestamp, end_timestamp)
		else:
			self.backend.get(namespace, start_timestamp, end_timestamp)

	def execute(self):
		"""Run after the setup method execution.

		You can also use this method in loop mode if you add to the above setup
		method a line like the following example:

			self.execute_as_loop(30)  # 30-second interval.
		"""

	def shutdown(self):
		"""Execute before tha NApp is unloaded."""
		log.info("Time Series NApp is shutting down.")

import time
teste = Main(KytosNApp)

#teste.save("TesteToday", "123", time.time())
os.system("influx -import -path=NOAA_data.txt -precision=s -database=NOAA_water_database")
#print(teste.backend.client.query("SELECT * FROM average_temperature"))
print(teste.get("average_temperature"))
