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
	erro = []
	while(i<quant_instancias):
		start = random.uniform(0, 1555953596)
		end = random.uniform(0, 1555953596)
		valor = random.uniform(0, 1000)
		if(start > end):
			e=inf.save('teste2.tes', valor, start)
		else:
			if i%2== 1:
				e = inf.save('teste2.tes', 'valor', end)
			e=inf.save('teste2.tes', valor, end)
		if(e is not None):
			erro.append(e)
		i=i+1
	print(len(erro))


inf = influx.InfluxBackend(settings)
popula_banco_teste(100)