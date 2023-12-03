from flask import request
from . import auth
from .models import AdminUser
from app.models import BaseResponse

from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required


@auth.route('/', methods=['POST'])
def admin_login():
    if not request.is_json:
        return BaseResponse(code=400, message='Missing JSON in request').dict()
    
    if not request.json.get('username'):
        return BaseResponse(code=400, message='Missing username parameter').dict()
    if not request.json.get('password'):
        return BaseResponse(code=400, message='Missing password parameter').dict()
    
    user_info = AdminUser.query.filter_by(username=request.json.get('username')).first()
    
    if not user_info:
        return BaseResponse(code=404, message='user not found').dict()
    
    if not user_info.verify_password(request.json.get('password')):
        return BaseResponse(code=400, message='password error').dict()
    
    token = create_access_token(identity=user_info.username, additional_claims={'role': user_info.level})
    
    return BaseResponse(data={'token': token, 'token_type': 'Bearer'}).dict()


@auth.route('/', methods=['GET'])
@jwt_required()
def get_admin_user_role():
    username = get_jwt_identity()
    user_info = AdminUser.query.filter_by(username=username).first()
    
    if not user_info:
        return BaseResponse(code=404, message='user not found').dict()
    return BaseResponse(data={'role': user_info.level, 'username': user_info.username}).dict()