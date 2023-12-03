from flask import abort, request, session
from app.utils import jwt_functions
from app.models import BaseResponse
import functools

# get bearer jwt token from http authorization header.
# verify it check if valid

def login_required(f):
    """
    Decorator that checks if the user is logged in.
    """
    def wrapper(*args, **kwargs):
        @functools.wraps(f)
        def decorator(*args, **kwargs):
            # Check if the token is present
            if not request.headers.get('Authorization'):
                return BaseResponse(code=401, message='No token').dict()

            # Get the token from the Authorization header
            token = request.headers.get('Authorization').split(' ')[1]

            # Verify the token
            payload = jwt_functions.verify_jwt(token)

            # Check if the token is valid
            if not payload:
                return BaseResponse(code=401, message='invalid token').dict()

            return f(*args, **kwargs)
        return decorator
    return wrapper

def role_required(roles):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Check if Authorization header exists
            if not request.headers.get('Authorization'):
                return BaseResponse(code=401, message='No token').dict()

            # Get JWT from Authorization header
            token = request.headers.get('Authorization').split(' ')[1]

            # Verify JWT
            payload = jwt_functions.verify_jwt(token)

            # Check if JWT is valid
            if not payload:
                return BaseResponse(code=401, message='invalid token').dict()

            # Check if user has required role
            if payload['role'] not in roles:
                return BaseResponse(code=401, message='permission denied').dict()

            # Return original function
            return f(*args, **kwargs)
        return wrapper
    return decorator

