import endpointer.http as ep_http

MESSAGE_TEXT = 'message-text'

def resource(request_verb, request_headers, request_uri, request_parameters, request_body, telemetry_data, api_module):
    
    match request_verb:

        case 'GET':

            return hello_world_message()

    return ep_http.method_not_allowed_response()

################################################ verb functions

def hello_world_message():

    return hello_world_message_response()

################################################ regular functions
################################################ input checking functions
################################################ response functions

def hello_world_message_response():

    response_headers = {}

    response_body = {
        MESSAGE_TEXT: 'Hello, World!'
    }

    return ep_http.ok_response(response_headers, response_body)

################################################ db functions
