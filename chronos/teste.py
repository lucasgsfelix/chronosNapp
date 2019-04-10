import settings


for i in settings.BACKENDS['INFLUXDB']:
	print(settings.BACKENDS['INFLUXDB'][i])