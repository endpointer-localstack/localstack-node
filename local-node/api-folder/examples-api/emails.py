import endpointer.telemetry as ep_telemetry
import endpointer.regexp as ep_regexp
import endpointer.http as ep_http

DOCS_URL = 'https://endpointer.com'

# Input fields

SENDER_NAME = 'Endpointer Localstack'
RECEIVER_EMAIL = 'receiver-email'
EMAIL_BODY = 'email-body'

EMAIL_SUBJECT = 'Endpointer Email Example'

# Response messages

INVALID_EMAIL = 'invalid-email'
INVALID_EMAIL_BODY = 'invalid-body'

SENT_MESSAGE_FIELD = 'result'
SENT_MESSAGE = 'email sent at: '

def resource(request_verb, request_headers, request_uri, request_parameters, request_body, telemetry_data, api_module):

    date_time = ep_telemetry.get_cluster_datetime(telemetry_data)

    match request_verb:

        case 'POST':

            return send_email(request_body, date_time, api_module)

    return ep_http.method_not_allowed_response()

################################################ verb functions   

def send_email(request_body, date_time, api_module):

    input_response = check_send_email_input(request_body, api_module)
    if input_response is not None:
        return input_response

    receiver_email = request_body.get(RECEIVER_EMAIL)
    email_body = request_body.get(EMAIL_BODY)

    try:
        api_module.send_email(SENDER_NAME, receiver_email, EMAIL_SUBJECT, email_body)

    except Exception as e:
        raise

    return send_email_ok_response(date_time)

################################################ regular functions
################################################ input checking functions

def check_send_email_input(request_body, api_module):

    receiver_email = request_body.get(RECEIVER_EMAIL)
    email_body = request_body.get(EMAIL_BODY)
    
    is_invalid_email = not ep_regexp.is_valid_email(receiver_email)
    is_invalid_body = (len(email_body) > 0)

    if is_invalid_email:

        response_headers = {}
        error_code = INVALID_EMAIL

        return ep_http.bad_request_response(response_headers, error_code, DOCS_URL)
    
    if not is_invalid_body:

        response_headers = {}
        error_code = INVALID_EMAIL_BODY

        return ep_http.bad_request_response(response_headers, error_code, DOCS_URL)
    
    return None

################################################ response functions

def send_email_ok_response(date_time):

    response_headers = {}

    sent_message = f'{SENT_MESSAGE} {date_time}'

    response_body = {
        SENT_MESSAGE_FIELD: sent_message
    }

    return ep_http.ok_response(response_headers, response_body)

