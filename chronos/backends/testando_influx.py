import influx
import sys
sys.path.append("..")
import settings
import time
from datetime import datetime
import random

def popula_banco_teste(quant_instancias):

	i = 0
	while(i<quant_instancias):
		start = random.uniform(0, 1555953596)
		end = random.uniform(0, 1555953596)
		valor = random.uniform(0, 1000)
		if(start > end):
			inf.save('teste.bool_teste', False, start)
			inf.save('teste.bool_teste', 'valor', start)
		else:
			inf.save('teste.bool_teste', False, end)
			inf.save('teste.bool_teste', 'valor', start)
		i=i+1
		exit()


inf = influx.InfluxBackend(settings)
random.seed()
#popula_banco_teste(100)
'''inf.save('teste.out', 123.12, '2019-03-15T18:38:39.648674048Z')
inf.save('teste.out', 123.12, '2019-03-15T18:38:39.648674048Z')
inf.save('teste.out', 123.12, '2019-03-15T18:38:39.648674048Z')
inf.save('teste.out', 123.12, '2019-03-15T18:38:39.648674048Z')
inf.save('teste.in', "string", '2019-03-15T18:38:39.648674048Z')'''
#print(inf.get('teste.out', 0, time.time()))
#inf.delete('teste', '2017-03-15', '2019-04-15')
print(inf.get('teste.out', None, None, 'mean', 'None', '1000d'))
