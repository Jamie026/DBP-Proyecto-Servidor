import json
from flask import make_response

def set_cookie(key, value):
    response_data = {
        "status": "success",
        "message": "Cookie created successfully"
    }
    response = make_response(json.dumps(response_data))
    response.set_cookie(key, str(value), secure=True, samesite="None")
    response.headers["Content-Type"] = "application/json"
    return response

def remove_cookie(key):
    response_data = {
        "status": "success",
        "message": "Cookie removed successfully"
    }
    response = make_response(json.dumps(response_data))
    response.set_cookie(key, "", secure=True, samesite="None", expires=0)
    response.headers["Content-Type"] = "application/json"
    return response

def validate_data(data, required_fields):
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True
