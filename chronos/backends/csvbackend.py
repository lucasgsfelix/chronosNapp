"""Backend that save data along time using a csv file"""
import os
import time
from datetime import datetime

import pandas as pd


def load_file(file):
    """load the file passing the name + the path."""
    try:
        dataframe = pd.read_csv(file, sep=',')
        dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'],
                                                errors='coerce')
    except(FileNotFoundError, IOError):
        assert "File Not Found"

    return dataframe


def put_value(value, store_value, timestamp, index):
    """Save a value in a dataframe."""
    store_value.loc[index, 'Value'] = value
    if timestamp is None:
        timestamp = datetime.utcfromtimestamp(time.time())
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        store_value.loc[index, 'Timestamp'] = timestamp


def delete(file_name, start_timestamp, end_timestamp):
    """ Delete a instances of the csv file"""
    dataframe = load_file(file_name)
    search = dataframe.Timestamp.dt.strftime('%Y-%m-%d %H:%M:%S')
    search = search.between(start_timestamp, end_timestamp)
    data_to_drop = dataframe[search]
    dataframe.drop(data_to_drop.index, inplace=True)
    dataframe.to_csv(file_name, sep=',', header=True, mode='w', inde=False)


def get(file_name, start_timestamp, end_timestamp):
    """Retrieve data from a csv file"""
    dataframe = load_file(file_name)
    search = dataframe.Timestamp.dt.strftime('%Y-%m-%d %H:%M:%S')
    search = search.between(start_timestamp, end_timestamp)
    return dataframe[search]


class CSVBackend:
    """CSV backend class. Defines methods to save,
    retrieve and delete data along time."""

    file_path = None
    user = 'user'

    def __init__(self, settings):
        """Define the a path in case the user does not pass one.
        Also defines the user getting from the backend."""

        self.file_path = settings.BACKENDS['CSV']['PATH']
        self.user = settings.BACKENDS['CSV']['USER']
        if self.file_path is None:
            if 'data' not in os.listdir():
                os.system('mkdir data')
                self.file_path = 'data/'
            else:
                self.file_path = 'data/'

        if self.file_path[len(self.file_path)-1] == '/':
            self.file_path = self.file_path + '/'

    def save(self, namespace, value, timestamp=None):
        """ Store the data in a .csv given a folder. """
        store_value = pd.DataFrame(columns=['Value', 'Timestamp'])
        if not isinstance(value, list):
            put_value(value, store_value, timestamp, 0)
        else:
            for index, val in enumerate(value):
                put_value(val, store_value, timestamp, index)

                file_path_name = (self.file_path + '/'+self.user +
                                  '_'+namespace+'.csv')

                file_name = self.user + '_' + namespace + '.csv'
                if file_name in os.listdir(self.file_path):
                    store_value.to_csv(file_path_name, sep=',', header=False,
                                       mode='a', index=False)
                else:
                    store_value.to_csv(file_path_name, sep=',', header=True,
                                       mode='w', index=False)
