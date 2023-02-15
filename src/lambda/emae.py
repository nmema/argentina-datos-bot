import urllib3
import json


API_BASE_URL = 'http://apis.datos.gob.ar/series/api/series' 

TIPO_DE_EMAE = {
    'BASE 2004': '143.3_NO_PR_2004_A_21',
    'BASE 2004 ajustado': '143.3_NO_PR_2004_A_31',
    'Var % mensual': '143.3_ICE_SER_VM_2004_A_34',
    'Var % interanual': '143.3_ICE_SERVIA_2004_A_25'
}

def lambda_handler(event, context):
    date = event['date']
    ids = ','.join(TIPO_DE_EMAE.values())
    request_url = f'{API_BASE_URL}?start_date={date}&end_date={date}&ids={ids}'

    http = urllib3.PoolManager()
    response = http.request('GET', request_url)
    data = json.loads(response.data)['data']  # output -> [[ date, emae ]]
    if len(data) == 0:
        emae_dict = {}
    else:
        emae_list = [0.0 if emae is None else emae for emae in data[0][1:]]
        emae_dict = dict(zip(TIPO_DE_EMAE.keys(), emae_list))
    return {'emae': emae_dict}
