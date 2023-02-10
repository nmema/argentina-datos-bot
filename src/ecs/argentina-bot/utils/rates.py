import urllib3
import json


API_BASE_URL = 'http://apis.datos.gob.ar/series/api/series'
TIPO_DE_CAMBIO = {
    'BNA': '168.1_T_CAMBIOR_D_0_0_26',
    'A3500': '168.1_T_CAMBI500_D_0_0_17',
    'ADRs': '168.1_T_CAMBIDRS_D_0_0_29',
    'MAE': '168.1_T_CAMBIMAE_D_0_0_15'
}

def lambda_handler(date):
    ids = ','.join(TIPO_DE_CAMBIO.values())
    request_url = f'{API_BASE_URL}?start_date={date}&end_date={date}&ids={ids}'
    
    http = urllib3.PoolManager()
    response = http.request('GET', request_url)
    data = json.loads(response.data)['data']  # output -> [[ date, rates ]]
    if len(data) == 0:
        rates_dict = {}
    else:
        rates_list = [0.0 if rate is None else rate for rate in data[0][1:]]
        rates_dict = dict(zip(TIPO_DE_CAMBIO.keys(), rates_list))
    return {'change_rates': rates_dict}