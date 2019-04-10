import influx
import settings
import os

def save_correto():
    pass
def save_batch():
    pass
def save_errado():
    pass

def get_correto(influx_backend):
    resultado = influx_backend.get("average_temperature")
    for i in resultado:
        print(i)

def get_intervalo():
    pass
def get_incorreto():
    pass
def delete_correto():
    pass
def delete_intervalo():
    pass
def delete_incorreto():
    pass

influx_backend = influx.InfluxBackend()

client = influx_backend.client


client.query("CREATE DATABASE db_teste")

os.system("influx -import -path=NOAA_data.txt -precision=s -database=NOAA_water_database")

#Testando inserções no banco
#influx_backend.client.query("USE db_teste")

get_correto(influx_backend)
client.query("DROP DATABASE db_teste")


