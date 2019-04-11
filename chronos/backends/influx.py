"""InfluxDB backend"""
from datetime import datetime

from influxdb import InfluxDBClient

from utils import Utils

def now():
    return datetime.utcnow().isoformat()

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
        """Delete the entire database --
        start_timestamp and end_timestamp most be a timestamp"""
        self._validate_namespace(namespace)
        utils_obj = Utils()
        utils_obj.validate_timestamp(start_timestamp, end_timestamp)
        self._delete_points(namespace, start_timestamp, end_timestamp)

    def get(self, namespace, start_timestamp=None, end_timestamp=None):
        """Make a query to retrieve something in the database."""
        self._validate_namespace(namespace)
        utils_obj = Utils()
        utils_obj.validate_timestamp(start_timestamp, end_timestamp)
        self._get_points(namespace, start_timestamp, end_timestamp)

    def _read_config(self, settings):
        
        self.params = {'HOST':None,'PORT':None:'USER':None,'PASS':None,'DBNAME':None}
        for i in settings.BACKENDS['INFLUXDB']:
            self.params[i] = settings.BACKENDS['INFLUXDB'][i]

        exist = list(filter(lambda x: x == None, self.params.values()))
        if len(exist): # exists None in the list
            if self.params['DBNAME'] is None:
                raise Exception("Error. Most specify database name.")
            
            if self.params['USER'] is None and self.params['PASS']:
                raise Exception("Error. Most specify user's login.")
            elif self.params['PASS'] and self.params['USER']:
                raise Exception("Error. Most specify user's password.")

    def _start_client(self):
        try:
            self._client = InfluxDBClient(host=self._host,
                                          port=self._port,
                                          username = self._username,
                                          password = self._password,
                                          database = self._database)
        except Exception:
            self._client = None # TODO: Tratar as exceptions

    def _create_database(self):
        try:
            self._client.create_database(self._db_name)
        except Exception:
            pass # TODO: Tratar as exceptions

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
        """Verify if a database exists"""
        all_dbs = self._client.get_list_database()
        exist = filter(lambda x: x['name'] == self._db_name, all_dbs)
        
        if exist:
            return exists[0]

        return False

    def _delete_points(self, namespace, start_timestamp, end_timestamp):

        query = {'query': 'DELETE FROM ' + namespace,
                'start':" WHERE time > '" + str(start_timestamp)+"'"
                'end':" and time < '"+str(end_timestamp)+"'"}

        result_query = self._query_assemble(query)

        self._client.query(delete_query)

    def _get_points(self, namespace, start_timestamp, end_timestamp):

        query = {'query': 'SELECT * FROM ' + namespace,
                'start':" WHERE time > '" + str(start_timestamp)+"'"
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

    def _validate_namespace(namespace):

        if namespace is None:
            raise Exception("Invalid namespace.")
        else:
            all_nspace = self._client.get_list_measurements()
            exist = filter(lambda x: x['name'] == self.namespace, all_nspace)
            if not exist:
                raise Exception("Required namespace does exist.")
