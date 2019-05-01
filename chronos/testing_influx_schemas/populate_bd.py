from influxdb import InfluxDBClient
from datetime import datetime
import random
from sys import argv

def case1(size_db, seed):
    print("\ncase1:\n")
    client = InfluxDBClient(database='case1') 
    random.seed(seed)
    erros = 0
    for i in range(size_db):
        namespace = ("kytos.telemetry.switches." + str(random.randint(1,10))+\
                     ".interfaces." + str(random.randint(1,10)) + ".bytes.in")
 
        timestamp = random.randint(1300000000000000000, 1600000000000000000)
        measurement = namespace
        field_name = 'value'
        field_value = random.randint(1000, 9999)
        
        data = [{                                                                
               'measurement': measurement,                    
               'time': timestamp,                                                     
               'fields': {field_name : field_value} 
                }]
        try:
            client.write_points(data)
        except:
            print("dados :", data)
            i = i -1
            erros = erros + 1
            continue
    print("Total de erros caso 1 = ", erros)


def case2(size_db, seed):
    print("\ncase2:\n")
    client = InfluxDBClient(database='case2')
    random.seed(seed)
    erros = 0
    for i in range(size_db):
        namespace = ("kytos.telemetry.switches."+str(random.randint(1,10))+\
                     ".interfaces."+str(random.randint(1,10))+".bytes.in")

        timestamp = random.randint(1300000000000000000,1600000000000000000)
        measurement = ('.').join(namespace.split('.')[:-1])
        field_name = ('.').join(namespace.split('.')[-1])
        field_value = random.randint(1000, 9999)

        data = [{                                                                
               'measurement': measurement,                    
               'time': timestamp,                                                     
               'fields': {field_name : field_value} 
                }]
        try:
            client.write_points(data)
        except:
            print("dados :", data)
            i = i -1
            erros = erros + 1
            continue
    print("Total de erros caso 2 = ", erros)

def case3(size_db, seed):
    print("\ncase3:\n")
    client = InfluxDBClient(database='case3')
    random.seed(seed)
    erros = 0
    for i in range(size_db):

        timestamp = random.randint(1300000000000000000,1600000000000000000)
        measurement = 'kytos.telemetry'
        switch = random.randint(1,10)
        interface = random.randint(1,250)
        bytes_in = random.randint(1000, 9999)

        data = [{                                                                
               'measurement': measurement,                    
               'time': timestamp,                                                     
               'fields': {'switches' : switch,
                          'interfaces' : interface,
                          'bytes_in' : bytes_in} 
                }]
        try:
            client.write_points(data)
        except:
            print("dados :", data)
            i = i -1
            erros = erros + 1
            continue

    print("Total de erros caso 3 = ", erros)

def case4(size_db, seed):
    print("\ncase4:\n")
    client = InfluxDBClient(database='case4')
    random.seed(seed)
    erros = 0
    for i in range(size_db):

        timestamp = random.randint(1300000000000000000,1600000000000000000)
        measurement = 'kytos.telemetry'
        switch = random.randint(1,10)
        interface = random.randint(1,10)
        bytes_in = random.randint(1000, 9999)
        bytes_out = random.randint(1000, 9999)

        data = [{                                                                
               'measurement': measurement,                    
               'time': timestamp,                                                     
               'tags': {'switches' : switch,
                         'interfaces' : interface,
                       },
               'fields': {'bytes_in' : bytes_in,
                          'bytes_out' : bytes_out
                         } 
                }]
        try:
            client.write_points(data)
        except:
            print("dados :", data)
            i = i -1
            erros = erros + 1
            continue
    print("Total de erros caso 4 = ", erros)


def case5(size_db, seed):
    print("\ncase5:\n")
    client = InfluxDBClient(database='case5')
    random.seed(seed)
    erros = 0
    for i in range(size_db):

        timestamp = random.randint(1500000000000000000,1600000000000000000)
        measurement = 'kytos.telemetry'
        switch = random.randint(1,10)
        interface = random.randint(1,10)
        bytes_in = random.randint(1000, 9999)
        bytes_out = random.randint(1000, 9999)

        data = [{                                                                
               'measurement': measurement,                    
               'time': timestamp,                                                     
               'tags': {'switches' : switch,
                        'interfaces' : interface,
                       },
               'fields': {'bytes_in' : bytes_in} 
                }]

        try:
            client.write_points(data)
        except:
            print("dados :", data)
            i = i -1
            erros = erros + 1
            continue
    print("Total de erros caso 5 = ", erros)





# list with sizes of measuments 1K, 10K, 100K, 1M, 10M, 100K, 1G
sizes_measurements = [1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000 ]
if argv[1] == "case1":
    case1(1000, 30)
elif argv[1] == "case2":
    case2(1000, 30)
elif argv[1] == "case3":
    case3(1000, 30)
elif argv[1] == "case5":
    case5(1000, 30)
'''
for size in sizes_measurements:
   case1(size, client, seed=30)
    case2(size, )
    case3(size, )
    case4(size, )
'''
