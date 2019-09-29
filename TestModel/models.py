import requests
import json

class Connect():
    code_config = {
        'url': 'https://cloud.minapp.com/api/oauth2/hydrogen/openapi/authorize/',
        'headers': {'Content-Type': 'application/json'}
    }
    code_data = {
        'client_id': '0e5d4e5846999c4b7cab',
        'client_secret': '397e56a9656b96f177c248d8804290d9aefcb35b'
    }
    token_config = {
        'url': 'https://cloud.minapp.com/api/oauth2/access_token/',
        'headers': {'Content-Type': 'application/json'}    
    }
    token_data = {
        'client_id': '0e5d4e5846999c4b7cab',
        'client_secret': '397e56a9656b96f177c248d8804290d9aefcb35b',
        'grant_type': 'authorization_code',
        'code': None
    }
    table_id = '78695'

    code_response = requests.post(url=code_config['url'], 
            data=json.dumps(code_data), 
            headers=code_config['headers'])
    token_data['code'] = code_response.json().get('code')
    token_response = requests.post(url=token_config['url'], 
            data=json.dumps(token_data), 
            headers=token_config['headers'])
    token = token_response.json().get('access_token')