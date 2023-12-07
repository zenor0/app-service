from flask import request
from . import goods
from .models import Good
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json
from datetime import datetime

from .schemas import UpdateGoodForm, CreateGoodForm

from flask_restful import Resource, Api

goodsApi = Api(goods)

class Goods(Resource):
    __decorators__ = []
    
    def get(self, good_id):
        good_info = Good.query.filter_by(good_id=good_id).first()

        if not good_info:
            return BaseResponse(code=404, message='good not found').dict()

        return BaseResponse(data=good_info.to_dict()).dict()

    def put(self, good_id):
        if 'application/json' not in request.content_type:
            return BaseResponse(code=400, message='content type must be application/json').dict()

        if not Good.query.filter_by(good_id=good_id).first():
            return BaseResponse(code=404, message='good not found').dict()

        if not request.data:
            return BaseResponse(code=400, message='request data is empty').dict()

        data = json.loads(request.data)
        
        if data['state']:
            data['state'] = Good.GOOD_STATES_ENUM[Good.GOOD_STATES_ENUM_DESCRIPTION.index(data['state'])]

        updateForm = UpdateGoodForm(**data)
        Good.query.filter_by(good_id=good_id).update(dict(updateForm))

        return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()

    def patch(self, good_id):
        if not Good.query.filter_by(good_id=good_id).first():
            return BaseResponse(code=404, message='good not found').dict()

        Good.query.filter_by(good_id=good_id).update({'state': Good.GOOD_STATES_ENUM[0]})

        return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()

class GoodsList(Resource):
    method_decorators = []
    def get(self):
        filter_condition = set()
        filter_condition.add(Good.game.like('%' + request.args.get('game', '', type=str) + '%'))
        filter_condition.add(Good.title.like('%' + request.args.get('title', '', type=str) + '%'))
        filter_condition.add(Good.detail.like('%' + request.args.get('detail', '', type=str) + '%'))
        # if request.args.get('state', '', type=str).lower() in Good.GOOD_STATES_ENUM_DESCRIPTION:
        #     state = Good.GOOD_STATES_ENUM_DESCRIPTION.index(request.args.get('state', '', type=str).lower())
        #     filter_condition.add(Good.state == Good.GOOD_STATES_ENUM[state])
        filter_condition.add(Good.state == Good.GOOD_STATES_ENUM_DESCRIPTION[1])

        if request.args.get('uid'):
            filter_condition.add(Good.good_id == request.args.get('uid', type=int))

        if request.args.get('seller_id'):
            filter_condition.add(Good.seller_id == request.args.get('seller_id'))

        order_by = request.args.get('order_by', '', type=str)
        order_list = ['asc', 'desc']
        if request.args.get('order', '') in order_list:
            order_by = order_by + ' ' + request.args.get('order', '')

        query_result = Good.query.order_by(text(order_by)).filter(and_(*filter_condition)).paginate(
            page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 12, type=int))
        
        # return BaseResponse().dict()

        return BaseResponse(data={'goods': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()
    def post(self):
        if 'application/json' not in request.content_type:
            return BaseResponse(code=400, message='content type must be application/json').dict()

        data = json.loads(request.data)
        createForm = CreateGoodForm(**data)
        result = Good().from_dict(dict(createForm))
        result.state = Good.GOOD_STATES_ENUM_DESCRIPTION[0]

        return BaseResponse(data=result.to_dict()).dict()


goodsApi.add_resource(Goods, '/<int:good_id>')
goodsApi.add_resource(GoodsList, '/')


@goods.route('/<int:good_id>/img', methods=['GET'])
def get_good_img(good_id):
    good_info =  Good.query.filter_by(good_id=good_id).first()
    if good_info == None:
        return BaseResponse(code=404, message='good not found').dict()
    

    return BaseResponse(data={'img': good_info.img_id}).dict()

@goods.route('/<int:good_id>/imgmap', methods=['GET'])
def get_good_imgmap(good_id):
    # if not Good.query.filter_by(good_id=good_id).first():
    #     return BaseResponse(code=404, message='good not found').dict()
    img_map = {}
    for i in range(1, 3):
        img_map['img'+str(i)] = "http://dummyimage.com/"+str(i*100)+"x"+str(i*100)
    return BaseResponse(data=img_map).dict()

@goods.route('/stats', methods=['GET'])
@jwt_required()
def get_good_stats():
    released_goods_count = len(Good.query.filter_by(state=Good.GOOD_STATES_ENUM[1]).all())
    total_goods_count = len(Good.query.all())
    
    ret_info = [{'value': total_goods_count-released_goods_count, 'name': '未上架'}, {'value': released_goods_count, 'name': '已上架'}]
    
    return BaseResponse(data={'stat': ret_info}).dict()


@goods.route('/', methods=['POST'])
def add_good():
    if 'application/json' not in request.content_type:
        return BaseResponse(code=400, message='content type must be application/json').dict()

    data = json.loads(request.data)
    createForm = CreateGoodForm(**data)
    result = Good().from_dict(dict(createForm))

    return BaseResponse(data=result.to_dict()).dict()

from werkzeug.utils import secure_filename
from flask import send_file
import os
from hashlib import md5

import io

UPLOAD_FOLDER = './uploads/imgs'
FILE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def check_file_extension(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in FILE_EXTENSIONS

def generate_img_id():
    return md5(str(datetime.utcnow()).encode('utf-8')).hexdigest()

@goods.route('/uploadImg', methods=['POST'])
def upload_img():
    if 'file' not in request.files:
        return BaseResponse(code=400, message='file not found').dict()
    
    file = request.files['file']
    if file.filename == None or file.filename == '':
        return BaseResponse(code=400, message='file not found').dict()
    if file and check_file_extension(file.filename):
        filename = generate_img_id() + '.' + secure_filename(file.filename).rsplit('.', 1)[1].lower()
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return BaseResponse(data={'img_id': filename}).dict()
    else:
        return BaseResponse(code=400, message='file type not supported').dict()
    
@goods.route('/img/<string:img_id>', methods=['GET'])
def get_img(img_id):
    if not os.path.isfile(os.path.join(UPLOAD_FOLDER, img_id)):
        return BaseResponse(code=404, message='img not found').dict()

    return send_file(io.FileIO(os.path.join(UPLOAD_FOLDER, img_id)), mimetype='image/jpeg')




@goods.route('/<int:good_id>/update', methods=['POST'])
# @jwt_required()
def update_good(good_id):
    if 'application/json' not in request.content_type:
        return BaseResponse(code=400, message='content type must be application/json').dict()

    if not Good.query.filter_by(good_id=good_id).first():
        return BaseResponse(code=404, message='good not found').dict()

    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()

    data = json.loads(request.data)
    
    if data['state']:
        data['state'] = Good.GOOD_STATES_ENUM[Good.GOOD_STATES_ENUM_DESCRIPTION.index(data['state'])]


    updateForm = UpdateGoodForm(**data)
    print(updateForm)
    Good.query.filter_by(good_id=good_id).update(dict(updateForm))

    return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()

@goods.route('/<int:good_id>/delete', methods=['GET'])
# @jwt_required()
def delete_good(good_id):
    if not Good.query.filter_by(good_id=good_id).first():
        return BaseResponse(code=404, message='good not found').dict()

    result = Good.query.filter_by(good_id=good_id).delete()

    return BaseResponse(data={'delete_count': result}).dict()
