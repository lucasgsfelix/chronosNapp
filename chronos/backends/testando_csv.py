import csvbackend
import settings
from datetime import datetime
obj = csvbackend.CSVBackend(settings)
obj.save('namespace_teste', 0, datetime.now())
#print(obj.delete('foo_namespace_teste', None, '2019-04-18T11:23:40.202591'))