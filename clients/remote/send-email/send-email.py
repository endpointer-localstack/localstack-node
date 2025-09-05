import json
import os
import endpointer.session as ep_session
import endpointer.lambdaf as ep_lambdaf
import requests

LAMBDA_ALIAS = 'send-email'

API_TOKEN = 'xDqTfnsMyHAjAoi'
LAMBDA_TOKEN = 'gITZNywljYe0TVT'

SESSION_TOKEN = os.environ.get(ep_session.SESSION_TOKEN_ENV)

url = "http://local.load.endpointer.com"

query_string = f'{ep_lambdaf.LAMBDA_ALIAS_FIELD}={LAMBDA_ALIAS}&{ep_lambdaf.LAMBDA_REFERENCE_FIELD}={API_TOKEN}.{LAMBDA_TOKEN}'

url = f'{url}?{query_string}'

headers = {
    "Content-Type": "application/json",
    ep_session.SESSION_TOKEN_HEADER:SESSION_TOKEN
}

body = {
    
    'receiver-email':'robertomessabrasil@gmail.com',
    'email-body':'Hello, World!',

}

def main():
    
    try:

        response = requests.post(url, headers=headers, json=body)
        response_status = response.status_code
        
        response_header_dict = dict(response.headers)
        response_headers = json.dumps(response_header_dict, indent='\t')

        print(f'Status Code: {response_status}')
        print(f'Headers: {response_headers}')

        response.raise_for_status()
        
        print_response(response)

    except requests.exceptions.RequestException as e:

        no_body = (response.status_code == 500) or (response.status_code == 403)
        if not no_body:
            print_response(response)

def print_response(response):

    response_json = response.json()
    response_body = json.dumps(response_json, indent='\t')

    print(response_body)

if __name__ == '__main__':
    main()
