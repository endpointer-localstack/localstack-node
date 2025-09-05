import os
import endpointer.session as ep_session

import json
import requests

REQUEST_VERB = 'GET'
API_TOKEN = 'cluster'
RESOURCE_TOKEN = 'stacktraces'

RESOURCE_ID = 'gITZNywljYe0TVT'

def main():

    load_manager_url = "http://local.stacktrace.endpointer.com:83"

    url = f'{load_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}/{RESOURCE_ID}'

    session_token = os.environ[ep_session.SESSION_TOKEN_ENV]

    headers = {
        ep_session.SESSION_TOKEN_HEADER:session_token
    }

    try:

        print(f'\n{REQUEST_VERB} {url}')
        
        response = requests.get(url, headers=headers)
        
        sent_headers = response.request.headers
        headers.update(sent_headers)
        print(headers)

        response_status = response.status_code
        
        response_header_dict = dict(response.headers)
        response_headers = json.dumps(response_header_dict, indent='\t')

        print(f'Status Code: {response_status}')
        print(f'Headers: {response_headers}')

        response.raise_for_status()
        
        # print_response(response)
        print_stacktrace(response)

    except requests.exceptions.RequestException as e:

        sent_headers = response.request.headers
        headers.update(sent_headers)
        print(headers)

        no_body = (response_status == 500) or (response_status == 403) or (response_status == 404)
        if not no_body:
            print_response(response)

def print_stacktrace(response):

    response_json = response.json()
    stacktrace_content_json = response_json['stacktrace-content']
    stacktrace_content = json.loads(stacktrace_content_json)

    print(stacktrace_content)

def print_response(response):

    response_json = response.json()
    response_body = json.dumps(response_json, indent='\t')

    print(response_body)


if __name__ == '__main__':
    main()
