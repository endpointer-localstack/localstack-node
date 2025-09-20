import endpointer.http as ep_http
import endpointer.session as ep_session

import requests
import mysql.connector as db

DOCS_URL = 'https://endpointer.com'

INVALID_SQL = 'invalid-sql'
INVALID_SESSION_TOKEN = 'invalid-session-token'

INVALID_SESSION_TOKEN = 'invalid-session-token'
INVALID_DB_TOKEN = 'invalid-db-token'
NO_ROLE = 'no-role'

DB_TOKEN = 'db-token'
SQL_COMMAND = 'sql-command'
ORGANIZATION_ROLE = 'organization-role'

REQUEST_VERB = 'GET'
API_TOKEN = 'cluster'
RESOURCE_TOKEN = 'dbs'
RESOURCE_ID = 'K7IMehV13K1z7ol'

################################################ regular functions

def has_privilege(session_token, db_token):

    (response_status, organization_role) = get_privilege(session_token, db_token)

    is_authorized = '200' in str(response_status)
    return is_authorized

def get_privilege(session_token, db_token):

    load_manager_url = "http://local.load.endpointer.com"

    url = f'{load_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}/{db_token}'

    headers = {
        ep_session.SESSION_TOKEN_HEADER:session_token
    }

    try:

        response = requests.get(url, headers=headers)
        
        response.raise_for_status()

        response_status = response.status_code

        response_json = response.json()

        role = response_json[ORGANIZATION_ROLE]

        return (response_status, role)
        
    except Exception as e:
        raise

def get_db_conn():

    db_conn = get_db_conn_local()
    
    return db_conn

def get_db_conn_remote():

    db_conn = db.connect(

        host='localhost',
        user='K7IMehV13K1z7ol_admin',
        password='LU1pBPYRL66dPF6',
        database='cluster'
    )

    return db_conn

def get_db_conn_local():
    
    db_conn = db.connect(

        host='192.168.122.156',
        user='admin_remote',
        password='admin',
        database='product'
    )
    
    return db_conn

################################################ input checking functions
################################################ response functions

def invalid_session_response():

    response_headers = {}

    error_code = INVALID_SESSION_TOKEN

    return ep_http.bad_request_response(response_headers, error_code, DOCS_URL)

def no_role_response():

    response_headers = {}

    error_code = NO_ROLE

    return ep_http.unauthorized_response(response_headers, error_code, DOCS_URL)

def invalid_session_response():

    response_headers = {}

    error_code = INVALID_SESSION_TOKEN

    return ep_http.bad_request_response(response_headers, error_code, DOCS_URL)

################################################ db functions
