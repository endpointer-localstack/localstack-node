import os
from pathlib import Path
import endpointer.http as ep_http
import endpointer.session as ep_session

import json
import requests

REQUEST_VERB = 'PATCH'

API_TOKEN = 'cluster'
RESOURCE_TOKEN = 'resources'
RESOURCE_ID = 'JnY0TgRZ8GY9xBz'

LOCAL_API_TOKEN = 'examples-api'
LOCAL_RESOURCE_TOKEN = 'messages.py'

API_FOLDER = 'local-node/api-folder'

def main():

    load_manager_url = "https://eur-001.endpointer.com"

    url = f'{load_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}/{RESOURCE_ID}'

    session_token = os.environ[ep_session.SESSION_TOKEN_ENV]

    request_headers = {

        ep_http.CONTENT_TYPE: ep_http.APPLICATION_JSON,
        ep_session.SESSION_TOKEN_HEADER:session_token

    }

    upload_content = get_upload_content()

    request_body = {

        'patch-op': 0,
        'uploaded-content': upload_content

    }

    try:

        print(f'\n{REQUEST_VERB} {url}')
        
        response = requests.patch(url, headers=request_headers, json=request_body)
        
        sent_headers = response.request.headers
        request_headers.update(sent_headers)
        print(request_headers)
        # print(f'{request_body}\n')

        response_status = response.status_code
        
        response_header_dict = dict(response.headers)
        response_headers = json.dumps(response_header_dict, indent='\t')

        print(f'Status Code: {response_status}')
        print(f'Headers: {response_headers}')

        response.raise_for_status()
        
        # print_response(response)

    except requests.exceptions.RequestException as e:

        is_500 = (response.status_code == 500)
        if is_500:
        
            sent_headers = response.request.headers
            request_headers.update(sent_headers)
            print(request_headers)
            # print(f'{request_body}\n')

        no_body = (response.status_code == 500) or (response.status_code == 404)
        if not no_body:
            print_response(response)

def get_upload_content():

    localstack_node_root = Path(__file__).resolve().parent.parent.parent

    file_path = f'{API_FOLDER}/{LOCAL_API_TOKEN}/{LOCAL_RESOURCE_TOKEN}'
    
    with open(file_path, 'r') as file:
        content = file.read()

    escaped_content = json.dumps(content)

    return escaped_content

def print_response(response):

    response_json = response.json()
    response_body = json.dumps(response_json, indent='\t')

    print(response_body)


if __name__ == '__main__':
    main()
