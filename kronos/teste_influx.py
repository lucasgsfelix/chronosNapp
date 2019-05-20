from backends.influx import InfluxBackend
import settings
import json

def _parse_result_set(result):
	
	if result:
		json_values = json.dumps(list(result)[0])
		return json_values

	return None


if __name__ == '__main__':

	inf = InfluxBackend(settings)
	result = inf.get('teste4.out')
	_parse_result_set(result)
