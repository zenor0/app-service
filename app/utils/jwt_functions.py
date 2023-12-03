import jwt
from app import Config
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

def expiry_date():
    return datetime.utcnow() + timedelta(seconds=Config.JWT_EXPIRY)

def generate_jwt(payload, expiry=expiry_date(), secret=None):
    """
    Generates a JWT token, using the given payload and expiry date,
    and the secret, if provided. The payload must be a dict; the expiry
    date must be a datetime object.
    """
    if not payload:
        raise ValueError('payload is required')
    
    # Set the payload's iss and exp claims.
    _payload = {
        'iss': "chat-service",
        'exp': expiry,
        }
    # Add the payload to the payload.
    _payload.update(payload)
    
    # If a secret was not provided, use the default.
    if not secret:
        secret = Config.JWT_SECRET
        
    # Create and return the access token.
    access_token = create_access_token(payload['username'], additional_claims=payload)
    return access_token


def verify_jwt(token, secret=None):
    # If no secret is provided, use the default secret
    if not secret:
        secret = Config.JWT_SECRET
        
    # Try to decode the token with the secret using the HS256 algorithm
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    # If the token has expired, set the payload to None
    except jwt.ExpiredSignatureError:
        payload = None
    # If the token is invalid, set the payload to None
    except jwt.InvalidTokenError:
        payload = None
    
    # Return the payload
    return payload
