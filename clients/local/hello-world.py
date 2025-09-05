import json
import requests

REQUEST_VERB = 'GET'
API_TOKEN = 'examples-api'
RESOURCE_TOKEN = 'messages'

def main():

    node_manager_url = "http://localstack.endpointer.com:82"

    url = f'{node_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}'

    headers = {}

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
        
        print_response(response)

    except requests.exceptions.RequestException as e:

        sent_headers = response.request.headers
        headers.update(sent_headers)
        print(headers)

        no_body = (response.status_code == 500)
        if not no_body:
            print_response(response)

def print_response(response):

    response_json = response.json()
    response_body = json.dumps(response_json, indent='\t')

    print(response_body)


if __name__ == '__main__':
    main()
