"""InfluxDB backend"""

import sys
import time
from datetime import datetime

from influxdb import InfluxDBClient

import settings

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

    #def delete(self, namespace, start_timestamp, end_timestamp=None):
    #    """Delete the entire database --
    #    start_timestamp and end_timestamp most be a timestamp"""
    #    delete_start_query = ('DELETE FROM ' + namespace + ' WHERE time >' +
    #                          str(start_timestamp))
    #    if start_timestamp is not None:
    #        delete_end_query = "' and time < '"+str(end_timestamp)+"'"
    #        Utils.validate_timestamp(start_timestamp, end_timestamp)
    #        self.client.query(delete_start_query+delete_end_query)
    #    else:
    #        self.client.query(delete_start_query)

    #def get(self, namespace, start_timestamp=None, end_timestamp=None):
    #    """Make a query to retrieve something in the database."""
    #    if start_timestamp is None:
    #        print("SELECT * FROM "+namespace)
    #        print(self.params)
    #        return self.client.query("SELECT * FROM "+namespace)

    #    time_start_query = ("SELECT value FROM " + namespace + " WHERE time >'" +
    #                        str(start_timestamp) + "'")
    #    
    #    if end_timestamp is not None:
    #        time_end_query = " and time < '"+str(end_timestamp)+"'"
    #        utils_obj = Utils()
    #        utils_obj.validate_timestamp(start_timestamp, end_timestamp)
    #        return self.client.query(time_start_query+time_end_query)
    #    print("query ",time_start_query)
    #    return self.client.query(time_start_query)

    def _read_config(self, settings):
        self._params = {}

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
            raise Exception("Database do not exists")

        try:
            self.client.write_points(data)
        except Exception:
            raise Exception("Error inserting data to InfluxDB.")

    def _get_database(self):
        """Verify if a database exists"""
        all_dbs = self.client.get_list_database()
        exist = filter(lambda x: x['name'] == self._db_name, all_dbs)
        
        if exist:
            return exists[0]

        return False
