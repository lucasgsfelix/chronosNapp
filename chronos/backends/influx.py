"""InfluxDB backend"""
from influxdb import InfluxDBClient

from utils import validate_timestamp, now

## telemetry
#
#kytos.telemetry.log.error = []
#kytos.telemetry.log.critical = []
#
#kytos.telemetry.switches.1.interfaces.232.bytes.in = (ts, value)
#
#kytos.telemetry.switches.1.interfaces.233.bytes_in = 
#kytos.telemetry.switches.1.interfaces.233.bytes_out = 
#kytos.telemetry.switches.1.interfaces.233.packets_in = 
#kytos.telemetry.switches.1.interfaces.233.packets_out = 
#
#backend.save(namespace, value, ts):
#backend.save(namespace, values, ts):
#    # Caso 1 :
#    measurement -> kytos.telemetry.switches.1.interfaces.232.bytes.in
#    fields -> "value" = value
#    
#    # Caso 2 :
#    measurement -> kytos.telemetry.switches.1.interfaces.232.bytes
#    fields -> "in" = value
#    
#    # Caso 3 :
#    measurement -> kytos.telemetry
#    fields -> "switch" = 1, "interface" = 232, "bytes_in" = 2000
#    
#    # Caso 4 :
#    measurement -> bytes
#    tags -> "switch" = 1, "interface" = 232
#    fields -> "in" = 2000, "out" = 300


class InfluxBackend:
    """This Backend is responsible to the connection with InfluxDB."""
    def __init__(self, settings):
        self._read_config(settings)
        self._start_client()

    def save(self, namespace, value, timestamp=None):
        """Insert the data on influxdb.

        In this case (InfluxDB), the last namespace will be the table.

        timestamp must be on ISO-8601 format.
        """
        timestamp = timestamp or now()
        
        data = {
         'measurement': '.'.join(namespace.split('.')[:-1]),
         'time': timestamp,
         'fields': {namespace.split('.')[-1]: value}
        }

        self._write_endpoints(data)

    def delete(self, namespace, start_timestamp=None, end_timestamp=None):
        """Delete the entire database.

        start_timestamp and end_timestamp most be a timestamp
        """
        if not self._namespace_exists('.'.join(namespace.split('.')[:-1])):
            raise Exception("Namespace {} does not exist".format(namespace))

        validate_timestamp(start_timestamp, end_timestamp)

        self._delete_points(namespace, start_timestamp, end_timestamp)

    def get(self, namespace, start_timestamp=None, end_timestamp=None):
        """Make a query to retrieve something in the database."""
        if not self._namespace_exists('.'.join(namespace.split('.')[:-1])):
            return None

        validate_timestamp(start_timestamp, end_timestamp)
        
        return self._get_points(namespace, start_timestamp, end_timestamp)

    def _read_config(self, settings):
        
        params = {'HOST': 'localhost',
                  'PORT': '8086',
                  'DBNAME': None,
                  'USER': None,
                  'PASS': None}

        config = settings.BACKENDS.get('INFLUXDB')

        for key in params:
            params.set(key, config.get(key, params['key']))

        if not params['DBNAME']:
            raise Exception("Error. Must specify database name.")

        self._host = params['HOST']
        self._port = params['PORT']
        self._username = params['USER']
        self._password = params['PASS']
        self._database = params['DBNAME']
       
    def _start_client(self):
        self._client = InfluxDBClient(host = self._host,
                                      port = self._port,
                                      username = self._username,
                                      password = self._password,
                                      database = self._database)

    def _create_database(self):
        self._client.create_database(self._database)

    def _write_endpoints(self, data, create_database=True):
        if not self._get_database() and create_database:
            self._create_database()
        else:
            raise Exception("Database do not exists.")

        try:
            self._client.write_points(data)
        except Exception:
            raise Exception("Error inserting data to InfluxDB.")

    def _get_database(self):
        """Verify if a database exists."""
        all_dbs = self._client.get_list_database()
        exist = filter(lambda x: x['name'] == self._db_name, all_dbs)
        
        if exist:
            return exists[0]

        return False

    def _delete_points(self, namespace, start_timestamp, end_timestamp):

        query = {'query': 'DELETE FROM ' + namespace,
                'start':" WHERE time > '" + str(start_timestamp)+"'",
                'end':" and time < '"+str(end_timestamp)+"'"}

        result_query = self._query_assemble(query)

        self._client.query(delete_query)

    def _get_points(self, namespace, start_timestamp, end_timestamp):

        query = {'query': 'SELECT * FROM ' + namespace,
                'start':" WHERE time > '" + str(start_timestamp)+"'",
                'end':" and time < '"+str(end_timestamp)+"'"}
        
        result_query = self._query_assemble(query)

        return self.client.query(time_start_query)

    def _query_assemble(self, query):

        if (not "'None'" in query['start']) and (not "'None'" in query['end']):
            result_query = query['query'] + query['start'] + query['end']
        elif not "'None'" in query['start']:
            result_query = query['query'] + query['start']
        elif not "'None'" in query['end']:
            result_query = query['query'] + query['end']
        else:
            result_query = query['query']

        return result_query

    def _namespace_exists(self, namespace):

        if namespace is None:
            raise Exception("Invalid namespace.")
        else:
            all_nspace = self._client.get_list_measurements()
            exist = filter(lambda x: x['name'] == namespace, all_nspace)
            if not exist:
                raise Exception("Required namespace does not exist.")
