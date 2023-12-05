from flask import request
from . import orders
from .models import Order
from ..goods.models import Good
from ..carts.models import Cart
from sqlalchemy import and_, extract, func
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json
from datetime import datetime, timedelta

from flask_restful import Resource, Api

orderApi = Api(orders)

class OrdersList(Resource):
    method_decorators = [jwt_required()]
    def get(self):
        filter_condition = set()
        if request.args.get('order_id'):
            filter_condition.add(Order.order_id == request.args.get('order_id'))
        if request.args.get('from_id'):
            filter_condition.add(Order.from_id == request.args.get('from_id'))
        if request.args.get('to_id'):
            filter_condition.add(Order.to_id == request.args.get('to_id'))
        if request.args.get('good_id'):
            filter_condition.add(Order.good_id == request.args.get('good_id'))
        if request.args.get('state', '', type=str).lower() in Order.ORDER_STATE_ENUM_DESCRIPTION:
            state = Order.ORDER_STATE_ENUM_DESCRIPTION.index(request.args.get('state', '', type=str).lower())
            print(state)
            filter_condition.add(Order.state == Order.ORDER_STATE_ENUM[state])
        
        order_by = request.args.get('order_by', '', type=str)
        order_list = ['asc', 'desc']
        if request.args.get('order') in order_list:
            order_by = order_by + ' ' + request.args.get('order', '')
        
        query_result = Order.query.order_by(text(order_by)).filter(and_(*filter_condition)).paginate(page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 20, type=int))
        
        return BaseResponse(data={'orders': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()   
        

orderApi.add_resource(OrdersList, '/')

@orders.route('/stats', methods=['GET'])
@jwt_required()
def get_order_stats():
    this_week = datetime.now().isocalendar()[1]
    this_month = datetime.now().month
    time_now = datetime.now()
    
    order_list_this_month = Order.query.filter(and_(Order.state == Order.ORDER_STATE_ENUM[2], time_now - timedelta(days=30) <= Order.pay_time)).all()
    order_list_last_month = Order.query.filter(and_(Order.state == Order.ORDER_STATE_ENUM[2], time_now - timedelta(days=60) <= Order.pay_time, Order.pay_time <= time_now - timedelta(days=30))).all()
    
    this_month_amount_array = []
    for i in range(1, 30):
        this_month_amount_array.append(sum([j.price for j in order_list_this_month if j.create_time.day == i]))
        
    last_month_amount_array = []
    for i in range(1, 30):
        last_month_amount_array.append(sum([j.price for j in order_list_last_month if j.create_time.day == i]))
        
    return BaseResponse(data={'this_month': this_month_amount_array, 'last_month': last_month_amount_array}).dict()


@orders.route('/<int:user_id>/<int:goods_id>', methods=['POST'])
def create_order(goods_id, user_id):
    goods_info = Good.query.filter_by(good_id=goods_id).first()
    if not goods_info:
        return BaseResponse(code=404, message='商品不存在').dict()

    if goods_info.state != Good.GOOD_STATES_ENUM_DESCRIPTION[1]:
        return BaseResponse(code=400, message='商品不可购买').dict()
    
    create_order = Order().from_dict({
        'from_id': goods_info.seller_id,
        'to_id': user_id,
        'good_id': goods_id,
        'price': goods_info.price,
        'state': Order.ORDER_STATE_ENUM[0],
        'create_time': datetime.now(),
        'pay_time': datetime.now(),
    })
    
    goods_info.state = Good.GOOD_STATES_ENUM_DESCRIPTION[3]

    from ..carts.views import delete_cart
    delete_cart(user_id, goods_id)

    return BaseResponse(data=create_order.to_dict()).dict()


@orders.route('/<int:user_id>/all', methods=['POST'])
def buy_all(user_id):
    goods_list = Cart.query.filter_by(user_id=user_id).all()
    resp_list = []
    for i in goods_list:
        good_info = Good.query.filter_by(good_id=i.goods_id).first()
        create_order = Order().from_dict({
            'from_id': good_info.seller_id,
            'to_id': user_id,
            'good_id': i.goods_id,
            'price': good_info.price,
            'state': Order.ORDER_STATE_ENUM[0],
            'create_time': datetime.now(),
            'pay_time': datetime.now(),
        })
        good_info.state = Good.GOOD_STATES_ENUM_DESCRIPTION[3]
        resp_list.append(good_info)
        
        from ..carts.views import delete_cart
        delete_cart(user_id, good_info.good_id)
        

    
    return BaseResponse(data={'goods' :[i.to_dict() for i in resp_list]}).dict()