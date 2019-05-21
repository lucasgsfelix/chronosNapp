from backends.influx import InfluxBackend
import settings
import json
import re

def _parse_result_set(result, field):
    
    if result:
        time_value, value = zip(*[(res['time'], res[field]) for res in list(result)[0]])
        return json.dumps([time_value, value])

    return None


if __name__ == '__main__':

    inf = InfluxBackend(settings)
    result = inf.get('teste2.out')
    #print(result)
    #saida =_parse_result_set(result, 'out')
    print(json.dumps(result[0]))
