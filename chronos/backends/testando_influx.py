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
			inf.save(31231, False, start)
			inf.save(' ', 'valor', start)
		else:
			inf.save(312312, False, end)
			inf.save(' ', 'valor', start)
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
print(inf.get('teste', 0, time.time(), 'mean', 'linear', '500d'))
