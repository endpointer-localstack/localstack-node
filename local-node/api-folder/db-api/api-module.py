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

# Local db
# --------------------------------
DB_SERVER = 'yourlocalip'
DB_DATABASE = 'yourlocaldb'

# Local db admin
# --------------------------------
DB_ADMIN = 'yourlocaldbadminuser'
DB_ADMIN_PASSWORD = 'yourlocaldbadminpassword'

# Local db user
# --------------------------------
DB_USER = 'yourlocaldb'
DB_USER_PASSWORD = 'yourlocaldbuserpassword'

# Remote db
# --------------------------------
# DB_SERVER = 'localhost'
# DB_DATABASE = 'yourdbtoken'

# Remote db admin
# --------------------------------
# DB_ADMIN = 'yourdbtoken_admin'
# DB_ADMIN_PASSWORD = 'youradminpassword'

# Remote db user
# --------------------------------
# DB_USER = 'yourdbtoken_user'
# DB_USER_PASSWORD = 'youruserpassword'

################################################ regular functions

def has_privilege(session_token, db_token):

    (response_status, organization_role) = get_privilege(session_token, db_token)

    is_authorized = '200' in str(response_status)
    return is_authorized

def get_privilege(session_token, db_token):

    load_manager_url = "https://eur-001.endpointer.com"

    url = f'{load_manager_url}/{API_TOKEN}/{RESOURCE_TOKEN}/{db_token}'

    query_string = f'query-op=0'

    url = f'{url}?{query_string}'

    headers = {
        ep_session.SESSION_TOKEN_HEADER:session_token
    }

    try:

        response = requests.get(url, headers=headers)
        
        response_status = response.status_code

        if '200' in str(response_status):

            response_json = response.json()

            role = response_json[ORGANIZATION_ROLE]

            return (response_status, role)
        
        return (response_status, None)
        
    except Exception as e:
        raise

def get_db_conn_admin():

    db_conn = db.connect(

        host=DB_SERVER,
        user=DB_ADMIN,
        password=DB_ADMIN_PASSWORD,
        database=DB_DATABASE
    )

    return db_conn

def get_db_conn():

    db_conn = db.connect(

        host=DB_SERVER,
        user=DB_USER,
        password=DB_USER_PASSWORD,
        database=DB_DATABASE
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
