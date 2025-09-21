import os
import endpointer.http as ep_http
import endpointer.session as ep_session

import json
import requests

REQUEST_VERB = 'GET'
API_TOKEN = '2CWaRwAjWJlHpDH'
RESOURCE_TOKEN = 'D8avvHm86pKGO03'

def main():

    node_manager_url = "https://eur-001.endpointer.com"

    url = f'{node_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}'

    db_token = '4H6NG07WssVsyea'
    sql_command = f'''
    
    SELECT
        COLUMN_NAME AS Field,
        COLUMN_TYPE AS Type,
        IS_NULLABLE AS Nullable,
        COLUMN_KEY AS Keyy,
        COLUMN_DEFAULT AS Defaultt,
        EXTRA AS 'Extra'
    FROM
        INFORMATION_SCHEMA.COLUMNS
    WHERE
        TABLE_SCHEMA = '{db_token}' AND TABLE_NAME = 'prod_product';
        
'''

    query_string = f'db-token={db_token}&sql-command={sql_command}'

    url = f'{url}?{query_string}'

    session_token = os.environ[ep_session.SESSION_TOKEN_ENV]

    request_headers = {
        ep_http.CONTENT_TYPE: ep_http.APPLICATION_JSON,
        ep_session.SESSION_TOKEN_HEADER:session_token
    }

    try:

        print(f'\n{REQUEST_VERB} {url}')
        
        response = requests.get(url, headers=request_headers)
        
        sent_headers = response.request.headers
        request_headers.update(sent_headers)
        print(request_headers) 

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

        no_body = (response.status_code == 500) or (response.status_code == 404)
        if not no_body:
            print_response(response)

def print_response(response):

    response_json = response.json()
    response_body = json.dumps(response_json)

    print(response_body)


if __name__ == '__main__':
    main()
