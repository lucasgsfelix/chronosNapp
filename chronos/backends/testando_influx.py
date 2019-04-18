import influx
import sys
sys.path.append("..")
import settings
import time
from datetime import datetime

inf = influx.InfluxBackend(settings)
#inf.save('teste.out', 123.12, '2019-03-15T18:38:39.648674048Z')
print(inf.get('teste.out', 0, time.time()))
#inf.delete('teste', '2017-03-15', '2019-04-15')
#print(inf.get('teste'))
