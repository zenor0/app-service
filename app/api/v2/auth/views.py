from flask import request
from . import auth
from .models import User
from app.models import BaseResponse
import json

from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required


@auth.route("/", methods=["POST"])
def login():
    if not request.is_json:
        return BaseResponse(code=400, message="Missing JSON in request").dict()

    if not request.json.get("username"):
        return BaseResponse(code=400, message="Missing username parameter").dict()
    if not request.json.get("password"):
        return BaseResponse(code=400, message="Missing password parameter").dict()

    user_info = User.query.filter_by(username=request.json.get("username")).first()

    if not user_info:
        return BaseResponse(code=404, message="user not found").dict()

    if not user_info.verify_password(request.json.get("password")):
        return BaseResponse(code=400, message="password error").dict()

    return BaseResponse(data=user_info.to_dict()).dict()


@auth.route("/register", methods=["POST"])
def register():
    if 'application/json' not in request.content_type:
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not request.json:
        return BaseResponse(code=400, message='Missing JSON in request').dict()
    
    if User.query.filter_by(username=request.json.get('username')).first():
        return BaseResponse(code=400, message='username already exists').dict()
    if User.query.filter_by(email=request.json.get('email')).first():
        return BaseResponse(code=400, message='email already exists').dict()

    data = json.loads(request.data)
    result = User().from_dict(dict(data))

    return BaseResponse(data=result.to_dict()).dict()