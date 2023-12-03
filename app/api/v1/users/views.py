from flask import request
from . import users
from .models import User
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

from ..goods.models import Good
from .schemas import UpdateUserForm

@users.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_info(user_id):
    user_info = User.query.filter_by(user_id=user_id).first()
    
    if not user_info:
        return BaseResponse(code=404, message='user not found').dict()
    return BaseResponse(data=user_info.to_dict()).dict()


@users.route('/', methods=['GET'])
@jwt_required()
def get_user_list():
    filter_condition = set()
    filter_condition.add(User._username.like('%' + request.args.get('username', '', type=str) + '%'))
    filter_condition.add(User.nickname.like('%' + request.args.get('nickname', '', type=str) + '%'))
    filter_condition.add(User._email.like('%' + request.args.get('email', '', type=str) + '%'))
    if request.args.get('realname', None, type=str):
        filter_condition.add(User.realname.like('%' + request.args.get('realname', '', type=str) + '%'))
    if request.args.get('id_number', None, type=str):
        filter_condition.add(User.id_number.like('%' + request.args.get('id_number', '', type=str) + '%'))
    if request.args.get('blocked', '', type=str).lower() in ['true', 'false']:
        filter_condition.add(User.blocked == (request.args.get('blocked', '', type=str).lower() == 'true'))
    if request.args.get('uid'):
        filter_condition.add(User.user_id == request.args.get('uid'))
    
    order_by = request.args.get('order_by', '', type=str)
    order_list = ['asc', 'desc']
    if request.args.get('order') in order_list:
        order_by = order_by + ' ' + request.args.get('order', '')
        
    query_result = User.query.order_by(text(order_by)).filter(and_(*filter_condition)).paginate(page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 20, type=int))
    # query_result = User.query.all()
    # return BaseResponse(data={'users': [i.to_dict() for i in query_result], 'count': len(query_result), 'page': 1}).dict()
    return BaseResponse(data={'users': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()



# add a new user
@users.route('/', methods=['POST'])
@jwt_required()
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


# modify user info
@users.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    if 'application/json' not in request.content_type:
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    print(request.data)
    data = json.loads(request.data)
    if not User.query.filter_by(user_id=user_id).first():
        return BaseResponse(code=404, message='user not found').dict()
    
    try:
        from .models import hash_and_salt_password
        hashed_password = hash_and_salt_password(data['password'])
        data.update({'password': hashed_password})
    except:
        pass
    
    updateForm = UpdateUserForm(**data)
    print(updateForm)
    User.query.filter_by(user_id=user_id).update(dict(updateForm))
    # User.query.filter_by(user_id=user_id).update({'blocked': True})
    
    return BaseResponse(data = User.query.filter_by(user_id=user_id).first().to_dict()).dict()


# change user authority
@users.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
def block_user(user_id):
    if not User.query.filter_by(user_id=user_id).first():
        return BaseResponse(code=404, message='user not found').dict()
    
    try:
        data = json.loads(request.data)
    except:
        return BaseResponse(code=400, message='invalid json').dict()
    
    
    if data['blocked'] not in [True, False]:
        return BaseResponse(code=400, message='blocked must be true or false').dict()
    
    User.query.filter_by(user_id=user_id).update({'blocked': data['blocked']})
    
    if data['blocked'] == True:
        goods_list = Good.query.filter_by(seller_id=user_id, state='released').all()
        for _ in goods_list:
             _.state = 'locked'
    
    return BaseResponse(data = User.query.filter_by(user_id=user_id).first().to_dict()).dict()


# delete user
@users.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if not User.query.filter_by(user_id=user_id).first():
        return BaseResponse(code=404, message='user not found').dict()
    
    user = User.query.filter_by(user_id=user_id).first()
    User.query.filter_by(user_id=user_id).first().delete()
    
    return BaseResponse(data=user.to_dict()).dict()