"""Module with the Constants used in the kytos/Cronos."""

DEFAULT_BACKEND = 'INFLUXDB'
BACKENDS = {}
BACKENDS['INFLUXDB'] = {
				'USER': 'foo',
				'PASS': 'bar',
				'PORT': 8086,
				'HOST': 'localhost',
                                'DBNAME':'NOAA_water_database'
}
BACKENDS['CSV'] = {
				'USER': 'foo',
				'PATH': 'data/'
}
