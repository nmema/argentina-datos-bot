import urllib3
import json


API_BASE_URL = 'http://apis.datos.gob.ar/series/api/series'
INFLATION_CODE = '101.1_I2NG_2016_M_22:percent_change'

def lambda_handler(event, context):
    end_date = event['date']
    year = end_date.split('-')[0]
    month = end_date.split('-')[1]
    if int(month) == 1:
        start_date = str(int(year) - 1) + '-' + '12'
    else:
        start_date = year + '-' + str(int(month) - 1).zfill(2)

    request_url = f'{API_BASE_URL}?start_date={start_date}&end_date={end_date}&ids={INFLATION_CODE}'

    http = urllib3.PoolManager()
    response = http.request('GET', request_url)
    data = json.loads(response.data)
    inflation = data['data']  # output -> [[ date, inflation ]]
    return {'inflation_rate': f'{inflation[0][1]:.02%}'}
