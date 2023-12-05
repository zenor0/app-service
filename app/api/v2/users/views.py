from flask import request
from . import users
from ..auth.models import User
from ..goods.models import Good
from ..orders.models import Order
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required, get_jwt_identity
import json


from pydantic import BaseModel
from typing import Optional

class UpdateUserForm(BaseModel):
    username: Optional[str]
    email: Optional[str]
    nickname: Optional[str]
    password: Optional[str]
    realname: Optional[str]
    id_number: Optional[str]
    blocked: Optional[bool]
    

@users.route('/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    user_info = User.query.filter_by(user_id=user_id).first()
    
    if not user_info:
        return BaseResponse(code=404, message='user not found').dict()
    return BaseResponse(data=user_info.to_dict()).dict()


@users.route('/<int:user_id>/goods', methods=['GET'])
def get_user_goods(user_id):
    user_info = User.query.filter_by(user_id=user_id).first()
    
    if not user_info:
        return BaseResponse(code=404, message='user not found').dict()
    
    goods = Good.query.filter_by(seller_id=user_id).all()
    return BaseResponse(data={'goods': [good.to_dict() for good in goods]}).dict()

@users.route('/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    user_info = User.query.filter_by(user_id=user_id).first()
    
    if not user_info:
        return BaseResponse(code=404, message='user not found').dict()
    
    orders = Order.query.filter_by(to_id=user_id).all()
    return BaseResponse(data={'orders': [order.to_dict() for order in orders]}).dict()

@users.route('/<int:user_id>/update', methods=['POST'])
def update_user(user_id):
    if 'application/json' not in request.content_type:
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    print(request.data)
    data = json.loads(request.data)
    if not User.query.filter_by(user_id=user_id).first():
        return BaseResponse(code=404, message='user not found').dict()
    
    try:
        from ..auth.models import hash_and_salt_password
        hashed_password = hash_and_salt_password(data['password'])
        data.update({'password': hashed_password})
    except:
        pass
    
    updateForm = UpdateUserForm(**data)
    print(updateForm)
    User.query.filter_by(user_id=user_id).update(dict(updateForm))
    # User.query.filter_by(user_id=user_id).update({'blocked': True})
    
    return BaseResponse(data = User.query.filter_by(user_id=user_id).first().to_dict()).dict()

@users.route('/', methods=['POST'])
# @jwt_required()
def add_user():
    if 'application/json' not in request.content_type:
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    data = json.loads(request.data)
    if User.query.filter_by(username=data['username']).first():
        return BaseResponse(code=400, message='username already exists').dict()
    if User.query.filter_by(email=data['email']).first():
        return BaseResponse(code=400, message='email already exists').dict()
    
    new_user = User().from_dict(data)
    
    return BaseResponse(data=new_user.to_dict()).dict()