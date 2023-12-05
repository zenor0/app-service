from flask import request
from . import carts
from .models import Cart
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json
import decimal

from flask_restful import Resource, Api

cartApi = Api(carts)

class Carts(Resource):
    method_decorators = []
    def get(self, user_id):
        query_result = Cart.query.filter_by(user_id=user_id).paginate(
            page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 10, type=int))
        
        return BaseResponse(data={'carts': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()
    
    

cartApi.add_resource(Carts, '/<int:user_id>')

@carts.route('/<int:user_id>/<int:goods_id>', methods=['POST'])
def add_cart(user_id, goods_id):
    result = Cart().from_dict({'user_id': user_id, 'goods_id': goods_id})
    
    if result.carts_id == None:
        return BaseResponse(code=400, message='cart already exists').dict()

    return BaseResponse(data=result.to_dict()).dict()
    
    
@carts.route('/<int:user_id>/<int:goods_id>/delete', methods=['POST'])
def delete_cart(user_id, goods_id):

    result = Cart.query.filter_by(user_id=user_id, goods_id=goods_id).first()
    if result == None:
        return BaseResponse(code=400, message='cart not exists').dict()
    else:
        result.delete()

    return BaseResponse(data=result.to_dict()).dict()