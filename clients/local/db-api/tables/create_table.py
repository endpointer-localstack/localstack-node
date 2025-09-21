import os
import endpointer.http as ep_http
import endpointer.session as ep_session

import json
import requests

REQUEST_VERB = 'POST'
API_TOKEN = 'db-api'
RESOURCE_TOKEN = 'tables'

def main():

    node_manager_url = "http://localstack.endpointer.com:82"

    url = f'{node_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}'

    session_token = os.environ[ep_session.SESSION_TOKEN_ENV]

    request_headers = {
        ep_http.CONTENT_TYPE: ep_http.APPLICATION_JSON,
        ep_session.SESSION_TOKEN_HEADER:session_token
    }

    request_body = {
    
        'db-token':'K7IMehV13K1z7ol',
        'sql-command':'''CREATE TABLE prod_product (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(20) NOT NULL
                        );'''

    }

    try:

        print(f'\n{REQUEST_VERB} {url}')
        
        response = requests.post(url, headers=request_headers, json=request_body)
        
        sent_headers = response.request.headers
        request_headers.update(sent_headers)
        print(request_headers)
        print(f'{request_body}\n')

        response_status = response.status_code
        
        response_header_dict = dict(response.headers)
        response_headers = json.dumps(response_header_dict, indent='\t')

        print(f'Status Code: {response_status}')
        print(f'Headers: {response_headers}')

        response.raise_for_status()
        
        print_response(response)

    except requests.exceptions.RequestException as e:

        is_500 = (response.status_code == 500)
        if is_500:
        
            sent_headers = response.request.headers
            request_headers.update(sent_headers)
            print(request_headers)
            print(f'{request_body}\n')

        no_body = (response.status_code == 500) or (response.status_code == 404)
        if not no_body:
            print_response(response)

def print_response(response):

    response_json = response.json()
    response_body = json.dumps(response_json, indent='\t')

    print(response_body)


if __name__ == '__main__':
    main()
