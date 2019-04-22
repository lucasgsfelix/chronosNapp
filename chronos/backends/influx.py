"""InfluxDB backend"""
from influxdb import InfluxDBClient

from utils import validate_timestamp, now, iso_format_validation


def _query_assemble(clause, namespace, start, end, field=None):

    if clause.upper() == 'SELECT':
        if field is None:
            clause = clause + ' * FROM ' + namespace
        else:
            clause = clause + " " + field + " FROM " + namespace

    elif clause.upper() == 'DELETE':
        clause = clause + ' FROM ' + namespace
    else:
        raise Exception('Error. Invalid clause.')

    if start is None and end is None:
        return clause

    time_clause = " WHERE time "
    if start is not None:
        clause = clause + time_clause + ">'" + str(start) + "'"
        if end is not None:
            clause = clause + " AND time <'" + str(end) + "'"
    else:
        clause = clause + time_clause + "<'" + str(end) + "'"

    #clause = "SELECT MEAN(out) FROM "+namespace+" WHERE time >= '"+str(start)+"' AND time <= '"+str(end)+"' GROUP BY time(1000d) fill(linear)"
    #print(clause)

    return clause


def _verify_namespace(namespace):
    field = None
    if '.' in namespace:
        field = namespace.split('.')[-1]
        namespace = '.'.join(namespace.split('.')[:-1])

    if field is None:
        field = 'kytos'
    return namespace, field


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
        timestamp = iso_format_validation(timestamp)
        namespace, field = _verify_namespace(namespace)
        self._verify_value_type(value, namespace, field)
        if isinstance(namespace, tuple):
            namespace = namespace[0]
        data = [{
            'measurement': namespace,
            'time': timestamp,
            'fields': {field: value}
        }]
        self._write_endpoints(data)

    def delete(self, namespace, start=None, end=None):
        """Delete the entire database.

        start and end most be a timestamp
        """
        start = iso_format_validation(start)
        end = iso_format_validation(end)
        namespace = _verify_namespace(namespace)
        if isinstance(namespace, tuple):
            namespace = namespace[0]
        if not self._namespace_exists(namespace):
            raise Exception("Namespace {} does not exist".format(namespace))

        validate_timestamp(start, end)

        self._delete_points(namespace, start, end)

    def get(self, namespace, start=None, end=None):
        """Make a query to retrieve something in the database."""
        start = iso_format_validation(start)
        end = iso_format_validation(end)
        namespace, field = _verify_namespace(namespace)
        if not self._namespace_exists(namespace):
            return None
        validate_timestamp(start, end)
        points = self._get_points(namespace, start, end, field)
        return points

    def _read_config(self, settings):

        params = {'HOST': 'localhost',
                  'PORT': '8086',
                  'DBNAME': None,
                  'USER': None,
                  'PASS': None}
        config = settings.BACKENDS.get('INFLUXDB')

        for key in params:
            params[key] = config.get(key, params[key])

        if not params['DBNAME']:
            raise Exception("Error. Must specify database name.")

        self._host = params['HOST']
        self._port = params['PORT']
        self._username = params['USER']
        self._password = params['PASS']
        self._database = params['DBNAME']

    def _start_client(self):

        self._client = InfluxDBClient(host=self._host,
                                      port=self._port,
                                      username=self._username,
                                      password=self._password,
                                      database=self._database)

    def _create_database(self):
        self._client.create_database(self._database)

    def _write_endpoints(self, data, create_database=True):

        if not self._get_database() and create_database:
            self._create_database()

        try:
            self._client.write_points(data)
        except Exception:
            raise Exception("Error inserting data to InfluxDB.")

    def _get_database(self):
        """Verify if a database exists."""
        all_dbs = self._client.get_list_database()
        exist = list(filter(lambda x: x['name'] == self._database, all_dbs))
        if not exist:
            return False

        return True

    def _delete_points(self, namespace, start, end):

        result = _query_assemble('DELETE', namespace, start, end)

        self._client.query(result)

    def _get_points(self, name, start, end, field=None):

        result = _query_assemble('SELECT', name, start, end, field)
        try:
            return self._client.query(result, chunked=True, chunk_size=0)
        except Exception:
            raise Exception("Error. Field '{}' not valid." .format(field))

    def _namespace_exists(self, namespace):

        if namespace is None:
            raise Exception("Invalid namespace.")
        else:
            all_nspace = self._client.get_list_measurements()
            if not all_nspace:
                raise Exception("Error. There are no valid database.")
            exist = list(filter(lambda x: x['name'] == namespace, all_nspace))
            if not exist:
                raise Exception("Required namespace does not exist.")
            else:
                return True

    def _verify_value_type(self, value, namespace, field):
        if isinstance(value, int):
            value = float(value)
        clause = "SHOW FIELD KEYS"
        result = self._client.query(clause)
        result = list(filter(lambda x: x['fieldKey'] == field, result[namespace]))
        result = result[0]['fieldType']
        if result == 'string':
            result = 'str'
        if type(value).__name__ != result:
            raise Exception("Error. The type of the field must be a '{}'."
                            .format(type(value).__name__))
        return value
