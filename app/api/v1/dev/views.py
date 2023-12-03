from flask import request
from . import dev

from ..goods.models import Good

from ..models import BaseResponse
from flask_jwt_extended import create_access_token
from app.utils import jwt_functions
from app import Config
import logging
import jwt
from ..auth.models import AdminUser

# @dev.route('/auth/<int:user_id>', methods=['GET'])
# def get_admin_token(user_id):
#     jwt_token = create_access_token(user_id)
#     return BaseResponse(data={'token': jwt_token}).dict()

@dev.route('/goods', methods=['PUT'])
def pass_all_censors():
    pending_goods = Good.query.filter_by(state=Good.GOOD_STATES_ENUM[0]).all()
    for _ in pending_goods:
        _.state = Good.GOOD_STATES_ENUM[1]
        
    return BaseResponse(data={'goods': [i.to_dict() for i in pending_goods]}).dict()

@dev.route('/auth/<int:user_id>', methods=['GET'])
def get_user_jwt(user_id):
    adminInfo = AdminUser.query.filter_by(admin_id=user_id).first()
    if not adminInfo:
        return BaseResponse(code=404, message='user not found').dict()
    
    token = jwt_functions.generate_jwt({'username': adminInfo.username, 'user_id': user_id, 'role': adminInfo.level})

    return BaseResponse(data={'token': token, 'token_type': 'Bearer'}).dict()

@dev.route('/auth/app/<int:user_id>', methods=['GET'])
def get_app_user_jwt(user_id):
    token = jwt.encode({'userid': user_id, 'blocked': False}, key='XianJuJWT', algorithm='HS256')
    # token = jwt_functions.generate_jwt({'userid': user_id, 'blocked': False}, secret='XianJuJWT')

    return BaseResponse(data={'token': token, 'token_type': 'Bearer'}).dict()

