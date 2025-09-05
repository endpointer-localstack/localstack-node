import os
import endpointer.session as ep_session

import json
import requests

REQUEST_VERB = 'GET'
API_TOKEN = 'cluster'
RESOURCE_TOKEN = 'telemetries'

RESOURCE_ID = 'resources'

def main():

    load_manager_url = "http://local.stacktrace.endpointer.com:84"

    url = f'{load_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}/{RESOURCE_ID}'

    session_token = os.environ[ep_session.SESSION_TOKEN_ENV]

    headers = {
        ep_session.SESSION_TOKEN_HEADER:session_token
    }

    try:

        response = requests.get(url, headers=headers)
        response_status = response.status_code
        
        response_header_dict = dict(response.headers)
        response_headers = json.dumps(response_header_dict, indent='\t')

        print(f'Status Code: {response_status}')
        print(f'Headers: {response_headers}')

        response.raise_for_status()
        
        print('\n')
        print_telemetry(response)

    except requests.exceptions.RequestException as e:

        no_body = (response_status == 500) or (response_status == 403) or (response_status == 404)
        if not no_body:
            print_response(response)

def print_telemetry(response):

    response_json = response.json()
    telemetry_content_json = response_json['telemetry-content']
    telemetry_content = json.loads(telemetry_content_json)

    print(telemetry_content)

def print_response(response):

    response_json = response.json()
    response_body = json.dumps(response_json, indent='\t')

    print(response_body)

if __name__ == '__main__':
    main()