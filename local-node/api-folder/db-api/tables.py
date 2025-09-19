import endpointer.telemetry as ep_telemetry
import endpointer.http as ep_http
import endpointer.regexp as ep_regexp
import endpointer.session as ep_session

def resource(request_verb, request_headers, request_uri, request_parameters, request_body, telemetry_data, api_module):

    session_token = ep_session.get_session_token(request_headers)
    no_session_token = session_token is None
    if no_session_token:
        return api_module.invalid_session_response()
    
    date_time = ep_telemetry.get_cluster_datetime(telemetry_data)

    match request_verb:

        case 'POST':

            return create_table(session_token, request_body, date_time, api_module)

        case 'GET':

            return desc_table(session_token, request_parameters, date_time, api_module)

    return ep_http.method_not_allowed_response()

################################################ verb functions

def desc_table(ssession_token, request_parameters, date_time, api_module):
    
    input_response = check_desc_table_input(request_parameters, api_module)
    if input_response is not None:
        return input_response
    
    db_token = request_parameters.get(api_module.DB_TOKEN)
    sql_command = request_parameters.get(api_module.SQL_COMMAND)

    # has_privilege = api_module.has_privilege(session_token, db_token)

    # if not has_privilege:

    #     return api_module.no_role_response()
    
    try:

        db_conn = api_module.get_db_conn()

        db_cursor = db_conn.cursor()

        table_description = desc_table_select(db_cursor, sql_command, api_module)

        column_list = []

        for column_info in table_description:

            column_list.append(column_info)

    except Exception as e:
        raise e

    finally:
        
        if db_cursor:
            db_cursor.close()
        
        if db_conn.is_connected():
            db_conn.close()

    return desc_table_ok_response(column_list)

def create_table(session_token, request_body, date_time, api_module):

    input_response = check_create_table_input(request_body, api_module)
    if input_response is not None:
        return input_response

    db_token = request_body.get(api_module.DB_TOKEN)
    sql_command = request_body.get(api_module.SQL_COMMAND)

    # has_privilege = api_module.has_privilege(session_token, db_token)

    # if not has_privilege:

    #     return api_module.no_role_response()

    try:

        db_conn = api_module.get_db_conn()

        db_cursor = db_conn.cursor()

        create_table_update(db_cursor, sql_command, api_module)

        db_conn.commit()

    except Exception as e:
        raise

    finally:
        
        if db_cursor:
            db_cursor.close()
        
        if db_conn.is_connected():
            db_conn.close()

    return ep_http.no_content_response()

################################################ regular functions
################################################ input checking functions

def check_desc_table_input(request_parameters, api_module):
    
    db_token = request_parameters.get(api_module.DB_TOKEN)
    sql = request_parameters.get(api_module.SQL_COMMAND)
   
    is_valid_db_token = (db_token is not None) and ep_regexp.is_valid_token(db_token)
    
    if not is_valid_db_token:

        response_headers = {}

        error_code = api_module.INVALID_DB_TOKEN

        return ep_http.bad_request_response(response_headers, error_code, api_module.DOCS_URL)

    
    is_invalid_sql = sql is None or (len(sql) == 0)

    if is_invalid_sql:

        response_headers = {}
        error_code = api_module.INVALID_SQL

        return ep_http.bad_request_response(response_headers, error_code, api_module.DOCS_URL)
    
    return None

def check_create_table_input(request_body, api_module):
    
    db_token = request_body.get(api_module.DB_TOKEN)
    sql = request_body.get(api_module.SQL_COMMAND)
   
    is_valid_db_token = (db_token is not None) and ep_regexp.is_valid_token(db_token)
    
    if not is_valid_db_token:

        response_headers = {}

        error_code = api_module.INVALID_DB_TOKEN

        return ep_http.bad_request_response(response_headers, error_code, api_module.DOCS_URL)

    
    is_invalid_sql = sql is None or (len(sql) == 0)

    if is_invalid_sql:

        response_headers = {}
        error_code = api_module.INVALID_SQL

        return ep_http.bad_request_response(response_headers, error_code, api_module.DOCS_URL)
    
    return None

################################################ response functions

def desc_table_ok_response(column_list):

    response_headers = {}

    response_body = column_list

    return ep_http.ok_response(response_headers, response_body)

################################################ db functions

def create_table_update(db_cursor, sql_command, api_module):

    db_cursor.execute(sql_command)

def desc_table_select(db_cursor, sql_command, api_module):

    db_cursor.execute(sql_command)
    row_set = db_cursor.fetchall()

    return row_set

