import endpointer.telemetry as ep_telemetry
import endpointer.http as ep_status
import endpointer.regexp as ep_regexp
import endpointer.http as ep_http

DOCS_URL = 'https://endpointer.com'

PRODUCT_ID = 'product-id'
PRODUCT_NAME = 'product-name'

INVALID_PRODUCT_ID = 'invalid-product-id'
INVALID_PRODUCT_NAME = 'invalid-product-name'

PATCH_OP = 'op'

OP_CHANGE_PRODUCT_NAME = 0

def resource(request_verb, request_headers, request_uri, request_parameters, request_body, telemetry_data, api_module):

    date_time = ep_telemetry.get_cluster_datetime(telemetry_data)

    match request_verb:

        case 'POST':

            return create_product(request_body, date_time, api_module)
            
        case 'PATCH':
                
            op = request_body.get(PATCH_OP)

            if op == OP_CHANGE_PRODUCT_NAME:
                return change_product_name(request_uri, request_body, date_time, api_module)
            
            return api_module.invalid_patch_operation_response()
        
        case 'DELETE':

            return delete_product(request_uri, date_time, api_module)
        
        case 'GET':

            is_product_detail = (len(request_uri) > 2)
            if is_product_detail:
                return product_detail(request_uri, api_module)
            
            return product_list(api_module)
        
    return ep_http.method_not_allowed_response()

################################################ verb functions

def product_detail(request_uri, api_module):

    input_response = check_account_detail_input(request_uri)
    if input_response is not None:
        return input_response
    
    product_id = request_uri[2]
    
    try:

        db_conn = api_module.get_db_conn()

        db_cursor = db_conn.cursor()

        product = get_product_by_id(db_cursor, product_id)

    except Exception as e:
        raise e

    finally:
        
        if db_cursor:
            db_cursor.close()
        
        if db_conn.is_connected():
            db_conn.close()

    return product_detail_ok_response(product, api_module)

def create_product(request_body, date_time, api_module):

    input_response = check_create_product_input(request_body, api_module)
    if input_response is not None:
        return input_response
    
    product_name = request_body.get(PRODUCT_NAME)

    try:

        db_conn = api_module.get_db_conn()

        db_cursor = db_conn.cursor()

        create_product_record(db_cursor, product_name, date_time, api_module)

        product_id = db_cursor.lastrowid

        db_conn.commit()

    except Exception as e:
        raise

    finally:
        
        if db_cursor:
            db_cursor.close()
        
        if db_conn.is_connected():
            db_conn.close()

    return product_created_ok_response(product_id, api_module)

def delete_product(request_uri, date_time, api_module):

    check_input_response = check_delete_product_input(request_uri, api_module)
    if check_input_response is not None:
        return check_input_response

    product_id = request_uri[2]

    try:

        db_conn = api_module.get_db_conn()

        db_cursor = db_conn.cursor()

        delete_product_record(db_cursor, product_id, date_time, api_module)

        db_conn.commit()

        has_deleted = (db_cursor.rowcount > 0)

        if not has_deleted:

            return ep_http.not_found_response()

    except Exception as e:
        raise

    finally:
        
        if db_cursor:
            db_cursor.close()
        
        if db_conn.is_connected():
            db_conn.close()

    return ep_http.no_content_response()

def change_product_name(request_uri, request_body, date_time, api_module):

    input_check_response = check_change_product_name_input(request_uri, request_body, api_module)
    if input_check_response is not None:
        return input_check_response
    
    product_id = request_uri[2]
    product_name = request_body[PRODUCT_NAME]

    try:

        db_conn = api_module.get_db_conn()

        db_cursor = db_conn.cursor()

        update_product_name(db_cursor, product_id, product_name, date_time, api_module)

        db_conn.commit()

        has_update = (db_cursor.rowcount > 0)

        if not has_update:

            return ep_http.not_found_response()

    except Exception as e:
        raise

    finally:
        
        if db_cursor:
            db_cursor.close()
        
        if db_conn.is_connected():
            db_conn.close()

    return ep_http.no_content_response()

def product_list(date_time, api_module):

    try:

        db_conn = api_module.get_db_conn()

        db_cursor = db_conn.cursor()

        product_id_list = get_product_id_list(db_cursor)

        product_list = []

        for (product_id, ) in product_id_list:

            product = get_product_by_id(db_cursor, product_id)

            (id, product_name) = product

            product_list.append({

                PRODUCT_ID:id,
                PRODUCT_NAME:product_name
            
            })

    except Exception as e:
        raise e

    finally:
        
        if db_cursor:
            db_cursor.close()
        
        if db_conn.is_connected():
            db_conn.close()

    return product_list_ok_response(product_list)

################################################ regular functions

################################################ input checking functions

def check_request_change_password_input(request_uri, api_module):
    
    email = request_uri[2] if (len(request_uri) > 2) else None
   
    is_valid_email = (email is not None) and ep_regexp.is_valid_email(email)
    
    if not is_valid_email:

        return api_module.invalid_email_response()
    
    return None

def check_resend_account_token_input(request_uri, api_module):
    
    email = request_uri[2] if (len(request_uri) > 2) else None
   
    is_valid_email = (email is not None) and ep_regexp.is_valid_email(email)
    
    if not is_valid_email:

        return api_module.invalid_email_response()
    
    return None

def check_account_detail_input(request_uri):
    
    product_id = request_uri[2] if (len(request_uri) > 2) else None
   
    is_valid_product_id = (product_id is not None) and isinstance(product_id, int)
    
    if not is_valid_product_id:

        response_headers = {}

        error_code = INVALID_PRODUCT_ID

        return ep_http.bad_request_response(response_headers, error_code, DOCS_URL)
    
    return None

def check_change_product_name_input(request_uri, request_body, api_module):

    product_id = request_uri[2] if (len(request_uri) > 2) else None
    product_name = request_body.get(PRODUCT_NAME)

    is_valid_product_id = (product_id is not None) and (isinstance(product_id, int))

    if not is_valid_product_id:

        return invalid_product_id_response()

    is_valid_product_name = (product_list is not None) and (len(product_name) > 0)

    if not is_valid_product_name:
        
        return invalid_product_name_response()
    
    return None

def check_delete_product_input(request_uri, request_body, api_module):

    product_id = request_uri[2] if (len(request_uri) > 2) else None

    is_valid_product_id = (product_id is not None) and (isinstance(product_id, int))

    if not is_valid_product_id:

        return invalid_product_id_response()
    
    return None

def check_create_product_input(request_body, api_module):

    product_name = request_body.get(PRODUCT_NAME)
    
    is_valid_product_name = ep_regexp.is_valid_token(product_name)

    if not is_valid_product_name:

        return invalid_product_name_response()
    
    return None

def check_confirm_account_input(request_uri, request_body, api_module):
    
    account_token = request_uri[2] if (len(request_uri) > 2) else None
    security_token = request_body.get(SECURITY_TOKEN)
    
    is_valid_account_token = (account_token is not None) and ep_regexp.is_valid_token(account_token)
    is_valid_security_token = (security_token is not None) and ep_regexp.is_valid_token(security_token)

    if not (is_valid_account_token and is_valid_security_token):

        return api_module.invalid_credentials_response()
    
    return None

################################################ response functions

def product_list_ok_response(product_list):

    response_headers = {}

    response_body = product_list

    return ep_http.ok_response(response_headers, response_body)

def invalid_product_id_response():

    response_headers = {}

    error_code = INVALID_PRODUCT_ID

    return ep_status.bad_request_response(response_headers, error_code, DOCS_URL)

def invalid_product_name_response():

    response_headers = {}

    error_code = INVALID_PRODUCT_NAME

    return ep_status.bad_request_response(response_headers, error_code, DOCS_URL)

def product_detail_ok_response(product, api_module):

    (product_id, product_name) = product

    response_headers = {}

    response_body = {

        PRODUCT_ID: product_id,
        PRODUCT_NAME: product_name

    }

    return ep_http.ok_response(response_headers, response_body)

def product_created_ok_response(product_id, api_module):

    response_headers = {}

    response_body = {
        PRODUCT_ID: product_id
    }

    return ep_http.ok_response(response_headers, response_body)

################################################ db functions

def get_product_by_id(db_cursor, product_id):

    sql_param = (product_id, )
    db_cursor.execute(SELECT_PRODUCT, sql_param)
    row = db_cursor.fetchone()

    is_found = row is not None
    if not is_found:
        return None

    return row

SELECT_PRODUCT = '''

    select id, name
      from prod_product
        where (id = %s)
        
'''

def get_product_id_list(db_cursor):

    db_cursor.execute(SELECT_PRODUCT_ID_LIST)
    row_set = db_cursor.fetchall()

    return row_set

SELECT_PRODUCT_ID_LIST = '''

    select id
      from prod_product
        
'''

def delete_product_record(db_cursor, product_id, date_time, api_module):

    sql_params = (product_id, )

    db_cursor.execute(DELETE_PRODUCT, sql_params)

DELETE_PRODUCT = '''
    
    delete from prod_product
     
     where (id = %s)

'''

def update_product_name(db_cursor, product_id, product_name, date_time, api_module):

    sql_params = (product_name, product_id)

    db_cursor.execute(UPDATE_PRODUCT_NAME, sql_params)

UPDATE_PRODUCT_NAME = '''
    
    update prod_product
     
     set
     
      name = %s
     
     where (id = %s)

'''

def create_product_record(db_cursor, product_name, date_time, api_module):

    sql_params = (product_name, )

    db_cursor.execute(INSERT_PRODUCT, sql_params)

INSERT_PRODUCT = '''

    insert into prod_product
     (name)
     values (%s)

'''
