from flask import request
from . import wallets
from .models import Wallet
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json
import decimal

@wallets.route('/', methods=['GET'])
@jwt_required()
def get_wallet_list():
    filter_condition = set()
    if request.args.get('user_id', None, type=int):
        filter_condition.add(Wallet.user_id == request.args.get('user_id'))
    if request.args.get('wallet_id', None, type=int):
        filter_condition.add(Wallet.wallet_id == request.args.get('wallet_id'))
    
    order_by = request.args.get('order_by', '', type=str)
    order_list = ['asc', 'desc']
    if request.args.get('order') in order_list:
        order_by = order_by + ' ' + request.args.get('order', '')
    
    query_result = Wallet.query.order_by(text(order_by)).filter(and_(*filter_condition)).paginate(
        page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 10, type=int))
    
    return BaseResponse(data={'wallets': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()


@wallets.route('/<int:wallet_id>', methods=['GET'])
@jwt_required()
def get_wallet_info(wallet_id):
    if not Wallet.query.filter_by(wallet_id=wallet_id).first():
        return BaseResponse(code=404, message='wallet not found').dict()

    return BaseResponse(data=Wallet.query.filter_by(wallet_id=wallet_id).first().to_dict()).dict()

@wallets.route('/<int:wallet_id>', methods=['PUT'])
@jwt_required()
def charge_wallet(wallet_id):
    # if request.content_type != 'application/json':
    #     return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not Wallet.query.filter_by(wallet_id=wallet_id).first():
        return BaseResponse(code=404, message='wallet not found').dict()
    
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    data = json.loads(request.data)
    
    if 'amount' not in data:
        return BaseResponse(code=400, message='amount is required').dict()
    
    wallet_info = Wallet.query.filter_by(wallet_id=wallet_id).first()
    wallet_info.balance += decimal.Decimal(data['amount'])
    wallet_info.save()
    
    return BaseResponse(data=wallet_info.to_dict()).dict()

@wallets.route('/<int:wallet_id>', methods=['DELETE'])
@jwt_required()
def withdraw_wallet(wallet_id):
    # if request.content_type != 'application/json':
    #     return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not Wallet.query.filter_by(wallet_id=wallet_id).first():
        return BaseResponse(code=404, message='wallet not found').dict()
    
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    data = json.loads(request.data)
    
    if 'amount' not in data:
        return BaseResponse(code=400, message='amount is required').dict()
    
    wallet_info = Wallet.query.filter_by(wallet_id=wallet_id).first()
    wallet_info.balance -= decimal.Decimal(data['amount'])
    wallet_info.save()
    
    return BaseResponse(data=wallet_info.to_dict()).dict()


@wallets.route('/<int:wallet_id>', methods=['PATCH'])
@jwt_required()
def block_wallet(wallet_id):
    # if request.content_type != 'application/json':
    #     return BaseResponse(code=400, message='content type must be application/json').dict()
    if not Wallet.query.filter_by(wallet_id=wallet_id).first():
        return BaseResponse(code=404, message='wallet not found').dict()
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    data = json.loads(request.data)
    if 'state' not in data:
        return BaseResponse(code=400, message='state is required').dict()
    if data['state'] not in Wallet.WALLET_STATES_ENUM:
        return BaseResponse(code=400, message='state is invalid').dict()
    
    wallet_info = Wallet.query.filter_by(wallet_id=wallet_id).first()
    wallet_info.state = data['state']
    
    return BaseResponse(data=wallet_info.to_dict()).dict()