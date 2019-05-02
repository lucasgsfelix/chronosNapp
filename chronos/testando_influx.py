import backends.influx as influx
import sys
import settings
import time
from datetime import datetime
import random
from kytos.core import KytosNApp
import main
from flask import Flask

def popula_banco_teste(quant_instancias):

	i = 0
	while(i<quant_instancias):
		start = random.uniform(0, 1555953596)
		end = random.uniform(0, 1555953596)
		valor = random.uniform(0, 1000)
		if(start > end):
			inf.save('teste2.out', False, start)
			inf.save('teste2.out', 'valor', start)
		else:
			inf.save('teste2.out', False, end)
			inf.save('teste2.out', 'valor', start)
		i=i+1
		exit()


inf = influx.InfluxBackend(settings)
popula_banco_teste(100)