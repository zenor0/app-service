from flask import request
from . import issues
from .models import Issue
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json


@issues.route('/', methods=['GET'])
@jwt_required()
def get_issue_list():
    filter_condition = set()
    # print(request.args.to_dict())
    if request.args.get('seller_id'):
        filter_condition.add(Issue.seller_id == request.args.get('seller_id'))
    if request.args.get('buyer_id'):
        filter_condition.add(Issue.buyer_id == request.args.get('buyer_id'))
    if request.args.get('judger_id'):
        filter_condition.add(Issue.issue_id == request.args.get('judger_id'))
    if request.args.get('judge_result') in Issue.JUDGE_RESULT_ENUM:
        filter_condition.add(Issue.judge_result == request.args.get('judge_result'))
    if request.args.get('state') in Issue.ISSUE_STATE_ENUM:
        filter_condition.add(Issue.state == request.args.get('state'))
        
    order = request.args.get('order_by')
    order_map = ['dec', 'asc']
    if request.args.get('order') in order_map:
        order = request.args.get('order') + order
    
    query_result = Issue.query.order_by(text(order)).filter(and_(*filter_condition)).paginate(page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 10, type=int)).items
    
    return BaseResponse(data={'users': [i.to_dict() for i in query_result]}).dict()


@issues.route('/<int:issue_id>', methods=['GET'])
@jwt_required()
def get_issue_info(issue_id):
    if not issue_id:
        return BaseResponse(code=400, message='issue_id is required').dict()
    
    if not Issue.query.filter_by(issue_id=issue_id).first():
        return BaseResponse(code=404, message='issue not found').dict()
    
    return BaseResponse(data=Issue.query.filter_by(issue_id=issue_id).first().to_dict()).dict()



@issues.route('/<int:issue_id>', methods=['PATCH'])
@jwt_required()
def judge_issue(issue_id):
    if not issue_id:
        return BaseResponse(code=400, message='issue_id is required').dict()
    if not Issue.query.filter_by(issue_id=issue_id).first():
        return BaseResponse(code=404, message='issue not found').dict()
    
    if request.json.get('judge_result') not in Issue.JUDGE_RESULT_ENUM:
        return BaseResponse(code=400, message='judge_result is invalid').dict()
    if request.json.get('judge_reason') is None:
        return BaseResponse(code=400, message='judge_reason is required').dict()
    
    issue = Issue.query.filter_by(issue_id=issue_id).first()
    issue.judge_result = request.json.get('judge_result')
    issue.judge_reason = request.json.get('judge_reason')
    
    issue.state = 'closed'
    
    return BaseResponse(data=issue.to_dict()).dict()
