from flask import make_response

def set_cookie(key, value):
    response = make_response("Cookie establecida")
    response.set_cookie(key, str(value), secure=True, samesite="None")
    return response

def remove_cookie(key):
    response = make_response("Cookie eliminada")
    response.set_cookie(key, "", secure=True, samesite="None", expires=0)
    return response

def validate_data(data, required_fields):
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True
