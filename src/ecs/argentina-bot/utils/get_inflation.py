import requests


API_BASE_URL = 'http://apis.datos.gob.ar/series/api/series'
INFLATION_CODE = '101.1_I2NG_2016_M_22:percent_change'

def handler(end_date):
    year = end_date.split('-')[0]
    month = end_date.split('-')[1]
    if int(month) == 1:
        start_date = str(int(year) - 1) + '-' + '12'
    else:
        start_date = year + '-' + str(int(month) - 1).zfill(2)

    request_url = f'{API_BASE_URL}?start_date={start_date}&end_date={end_date}&ids={INFLATION_CODE}'
    response = requests.get(request_url)
    inflation = response.json()['data']  # output -> [[ date, inflation ]]
    return f'{inflation[0][1]:.02%}'
