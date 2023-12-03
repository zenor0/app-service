from flask import request
from . import admins
from ..auth.models import AdminUser
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json

from app.decorators import role_required
from .schemas import CreateAdminForm

@admins.route('/', methods=['GET'])
@role_required(['superuser'])
def get_admin_list():
    
    admin_list = AdminUser.query.all()
    
    return BaseResponse(data={'admins': [i.to_dict() for i in admin_list]}).dict()


@admins.route('/<int:admin_id>', methods=['GET'])
@role_required(['superuser'])
def get_admin_info(admin_id):
    if not AdminUser.query.filter_by(admin_id=admin_id).first():
        return BaseResponse(code=404, message='admin not found').dict()
    
    admin_info = AdminUser.query.filter_by(admin_id=admin_id).first()
    
    return BaseResponse(data=admin_info.to_dict()).dict()


@admins.route('/', methods=['POST'])
@role_required(['superuser'])
def create_admin():
    if 'application/json' not in request.content_type:
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    try:
        formData = CreateAdminForm(**json.loads(request.data))
    except Exception as e:
        return BaseResponse(code=400, message='form format error').dict()
    
    result = AdminUser(**formData.dict()).save()
    
    if not result.admin_id:
        return BaseResponse(code=400, message='username already exists').dict()
    
    return BaseResponse(data=result.to_dict()).dict()

@admins.route("/<int:admin_id>", methods=["PUT"])
@role_required(['superuser'])
def modify_admin(admin_id):
    if 'application/json' not in request.content_type:
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not AdminUser.query.filter_by(admin_id=admin_id).first():
        return BaseResponse(code=404, message='admin not found').dict()
    
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    try:
        formData = CreateAdminForm(**json.loads(request.data))
    except Exception as e:
        return BaseResponse(code=400, message='form format error').dict()
    
    try:
        from ..auth.models import hash_and_salt_password
        hashed_password = hash_and_salt_password(formData.password)
        formData.password = hashed_password
    except:
       return BaseResponse(code=400, message='password error').dict()
    
    AdminUser.query.filter_by(admin_id=admin_id).update(formData.dict())
    
    return BaseResponse(data=AdminUser.query.filter_by(admin_id=admin_id).first().to_dict()).dict()

