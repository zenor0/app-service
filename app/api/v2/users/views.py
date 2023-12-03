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