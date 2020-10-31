def login_required(func):
    
    logged_out_response = {
        "logout": {
            "status": "failure",
            "message": "user is not logged in"
        }
    }

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        login_req_auth_token = request.cookies.get("auth-token")
        
        saved_auth_token_array = user_auth_logs.objects(auth_token=login_req_auth_token)
        
        if saved_auth_token_array:
            saved_auth_log_object = saved_auth_token_array[0]
            if saved_auth_log_object.auth_token == login_req_auth_token:
                saved_last_login_date_time = saved_auth_log_object.last_login_date_time
                if isSessionAlive(saved_last_login_date_time, datetime.today()):
                    return func(*args, **kwargs)

        return logged_out_response

    return wrapper


def pre_login_check(func):

    logged_in_response = {
        "login": {
            "status": "success",
            "message": "user is already logged in"
        }
    }

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        login_req_auth_token = request.cookies.get("auth-token")
        saved_auth_token_array = user_auth_logs.objects(auth_token=login_req_auth_token)
        if saved_auth_token_array:
            saved_auth_log_object = saved_auth_token_array[0]
            if saved_auth_log_object.auth_token == login_req_auth_token:
                saved_last_login_date_time = saved_auth_log_object.last_login_date_time
                if isSessionAlive(saved_last_login_date_time, datetime.today()):
                    return logged_in_response
        return func(*args,**kwargs)
    return wrapper
