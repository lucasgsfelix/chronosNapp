"""Module with the Constants used in the kytos/Cronos."""

DEFAULT_BACKEND = 'INFLUXDB'

BACKENDS = {
    'INFLUXDB': {'USER': 'foo',
                 'PASS': 'bar',
                 'DBNAME': 'NOAA_water_database'},
    'CSV': {'USER': 'foo',
            'PATH': 'data/' }
}
