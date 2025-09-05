import endpointer.http as ep_http

import json
import requests

REQUEST_VERB = 'POST'
API_TOKEN = 'aA3cAZxgEnUYIBq'
RESOURCE_TOKEN = 'W90rygJWNu9zHVr'

def main():

    load_manager_url = "http://local.load.endpointer.com"

    url = f'{load_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}'

    request_headers = {
        ep_http.CONTENT_TYPE: ep_http.APPLICATION_JSON
    }

    request_body = {
    
        'receiver-email':'robertomessabrasil@gmail.com',
        'email-body':'Hello, World!',

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
