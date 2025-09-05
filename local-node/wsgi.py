from datetime import datetime as date_time
import endpointer.http as ep_http
import endpointer.cluster as ep_cluster
import endpointer.http as ep_http
import endpointer.resource as ep_resource

from http import HTTPStatus as http_status

import importlib
import json
import os

DOCS_URL = 'https://endpointer.com'

API_FOLDER = 'api-folder'
API_MODULE = 'api-module'

def application(environ, start_response):

    request_verb = ep_http.get_request_verb(environ)

    is_options = (request_verb == 'OPTIONS')
    
    if is_options:

        (response_status, response_headers, response_body) = prepare_options_response()
        print((response_status, response_headers, response_body))
        start_response(
            response_status,
            response_headers
        )
        
        return response_body

    request_headers = ep_http.get_request_headers(environ)

    request_uri = ep_http.get_request_uri(environ)

    request_parameters = ep_http.get_request_parameters(environ)

    dt = date_time.now()

    telemetry_data = {
        ep_cluster.CLUSTER_DATA: {
            ep_cluster.CLUSTER_DATETIME: ep_http.format_datetime(dt)
        }
    }

    api_token = request_uri[0]

    resource_token = request_uri[1]

    current_folder = os.path.dirname(__file__)

    api_path = f'{API_FOLDER}.{api_token}'

    api_folder = f'{current_folder}/{API_FOLDER}/{api_token}'

    api_module_file = f'{api_folder}/{API_MODULE}.py'
    
    resource_file = f'{api_folder}/{resource_token}.py'
    
    is_options = os.path.exists(api_module_file) and os.path.exists(resource_file)
    
    if not is_options:

        (response_status, response_headers, response_body) = not_found_response()
        
        start_response(
            response_status,
            response_headers
        )

        return response_body
    
    api_module_path = f'{api_path}.{API_MODULE}'
 
    resource_path = f'{api_path}.{resource_token}'

    try:

        api_module = importlib.import_module(api_module_path)

        function_module = importlib.import_module(resource_path)

        request_body = ep_http.get_request_body(environ)

        response = function_module.resource(request_verb, request_headers, request_uri, request_parameters, request_body, telemetry_data, api_module)

    except Exception as e:

        print(e)

        (response_status, response_headers, response_body) = internal_server_error_response()

        start_response(
            response_status,
            response_headers
        )

        return response_body
    
    response_status = response[ep_http.RESPONSE_STATUS]

    is_no_content = (response_status is http_status.NO_CONTENT)
    if is_no_content:

        (response_status, response_headers, response_body) = no_content_response(response)

        start_response(
            response_status,
            response_headers
        )

        return response_body
    
    try:
    
        (response_status, response_headers, response_body) = prepare_response_with_body(response)

        start_response(
            response_status,
            response_headers
        )

        return response_body
    
    except Exception as e:

        print(e)

        (response_status, response_headers, response_body) = internal_server_error_response()

        start_response(
            response_status,
            response_headers
        )

        return response_body

def prepare_response_with_body(response):

    response_status = response[ep_http.RESPONSE_STATUS]
    response_headers = response[ep_http.RESPONSE_HEADERS]

    response_status_string = f'{response_status.value} {response_status.phrase}'

    response_body = response[ep_http.RESPONSE_BODY]
    response_body_string = json.dumps(response_body)
    response_body_bytes = response_body_string.encode(ep_http.UTF_8)

    response_headers[ep_http.CONTENT_TYPE] = ep_http.APPLICATION_JSON
    response_headers[ep_http.CONTENT_LENGTH] = str(len(response_body_string))
    
    response_headers_list = list(response_headers.items())

    return (response_status_string, response_headers_list, [response_body_bytes])

def internal_server_error_response():

    response_status = http_status.INTERNAL_SERVER_ERROR.value
    response_reason = http_status.INTERNAL_SERVER_ERROR.phrase
    response_headers = []

    response_status_string = f'{response_status} {response_reason}'

    response_body_bytes = []
    
    return (response_status_string, response_headers, response_body_bytes)

def no_content_response(response):

    response_status = response[ep_http.RESPONSE_STATUS]
    response_headers = response[ep_http.RESPONSE_HEADERS]
    
    response_status_string = f'{response_status.value} {response_status.phrase}'
    response_headers_list = list(response_headers.items())

    response_body_bytes = []

    return (response_status_string, response_headers_list, response_body_bytes)

def not_found_response():

    response_headers = {}

    response_body = {

        ep_http.ERROR_CODE_FIELD:ep_resource.RESOURCE_NOT_DEPLOYED,
        ep_http.DOCS_URL_FIELD:DOCS_URL

    }

    response =  {

        ep_http.RESPONSE_STATUS: http_status.NOT_FOUND,
        ep_http.RESPONSE_HEADERS: response_headers,
        ep_http.RESPONSE_BODY: response_body

    }

    return prepare_response_with_body(response)
    
def prepare_options_response():
    
    response_status = http_status.NO_CONTENT
    response_reason = http_status.NO_CONTENT.phrase
    response_headers = {
        
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Max-Age':'86400',
        'Content-Length': '0'

    }

    response_status_string = f'{response_status} {response_reason}'

    response_headers_list = list(response_headers.items())

    return (response_status_string, response_headers_list, [])