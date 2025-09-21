import endpointer.http as ep_http
import json
import requests

REQUEST_VERB = 'DELETE'
API_TOKEN = 'db-api'
RESOURCE_TOKEN = 'products'
RESOURCE_ID = '1'

def main():

    load_manager_url = "http://localstack.endpointer.com:82"

    url = f'{load_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}/{RESOURCE_ID}'

    request_headers = {
        ep_http.CONTENT_TYPE: ep_http.APPLICATION_JSON
    }

    try:

        print(f'\n{REQUEST_VERB} {url}')
        
        response = requests.delete(url, headers=request_headers)
        
        sent_headers = response.request.headers
        request_headers.update(sent_headers)
        print(request_headers)

        response_status = response.status_code
        
        response_header_dict = dict(response.headers)
        response_headers = json.dumps(response_header_dict, indent='\t')

        print(f'Status Code: {response_status}')
        print(f'Headers: {response_headers}')

        response.raise_for_status()
        
        # print_response(response)

    except requests.exceptions.RequestException as e:

        sent_headers = response.request.headers
        request_headers.update(sent_headers)
        print(request_headers)

        no_body = (response.status_code == 500)
        if not no_body:
            print_response(response)

def print_response(response):

    response_json = response.json()
    response_body = json.dumps(response_json, indent='\t')

    print(response_body)


if __name__ == '__main__':
    main()
