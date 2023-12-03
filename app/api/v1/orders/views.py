from flask import request
from . import orders
from .models import Order
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json


@orders.route('/', methods=['GET'])
@jwt_required()
def get_order_list():
    filter_condition = set()
    # print(request.args.to_dict())
    if request.args.get('order_id'):
        filter_condition.add(Order.order_id == request.args.get('order_id'))
    if request.args.get('from_id'):
        filter_condition.add(Order.from_id == request.args.get('from_id'))
    if request.args.get('to_id'):
        filter_condition.add(Order.to_id == request.args.get('to_id'))
    if request.args.get('good_id'):
        filter_condition.add(Order.good_id == request.args.get('good_id'))
    if request.args.get('state') in Order.ORDER_STATE_ENUM:
        filter_condition.add(Order.state == request.args.get('state'))
    
    order_by = request.args.get('order_by', '', type=str)
    order_list = ['asc', 'desc']
    if request.args.get('order') in order_list:
        order_by = order_by + ' ' + request.args.get('order', '')
    
    query_result = Order.query.order_by(text(order_by)).filter(and_(*filter_condition)).paginate(page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 20, type=int))
    
    return BaseResponse(data={'orders': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()
