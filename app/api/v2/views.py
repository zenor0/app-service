from . import api
import jsonpickle
import os

from .models import BaseResponse, RouteItem, RouteMeta, DashboardPanel
# from .users.models import User
from .goods.models import Good
from .auth.models import User
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import json, requests

from datetime import datetime
start_time = datetime.utcnow()

@api.route('/menu', methods=['GET'])
@jwt_required()
def get_menu_list():
    username = get_jwt_identity()
    user_info = User.query.filter_by(username=username).first()
    
    router_list = []
    # if user_info:
    #     router_list.append(RouteItem(path='/censor2', name='censor2', component='LAYOUT', meta=RouteMeta(title=f'{user_info.username}:{user_info.level}', icon='user-talk'), 
    #                              children=[RouteItem(path='good', name='CensorGood', component='/censor/good/index', meta=RouteMeta(title='货物审核')), 
    #                                     #    RouteItem(path='user', name='CensorUser', component='/censor/user/index', meta=RouteMeta(title='用户审核'))
    #                                        ]))
    
    router_list.append(RouteItem(path='/censor', name='censor', component='LAYOUT', meta=RouteMeta(title='审核管理', icon='user-talk'), 
                                 children=[RouteItem(path='good', name='CensorGood', component='/censor/good/index', meta=RouteMeta(title='货物审核')), 
                                        #    RouteItem(path='user', name='CensorUser', component='/censor/user/index', meta=RouteMeta(title='用户审核'))
                                           ]))
    router_list.append(RouteItem(path='/app', name='app', component='LAYOUT', meta=RouteMeta(title='业务管理', icon='app'),
                                 children=[RouteItem(path='user', name='AppUser', component='/app/user/index', meta=RouteMeta(title='用户管理')),
                                           RouteItem(path='user/create', name='AppCreateUser', component='/app/user/createForm/index', meta=RouteMeta(title='创建用户', hidden=True)),
                                           RouteItem(path='user/edit', name='AppEditUser', component='/app/user/editForm/index', meta=RouteMeta(title='编辑用户', hidden=True)),
                                           RouteItem(path='good', name='AppGood', component='/app/good/index', meta=RouteMeta(title='货物管理')),
                                           RouteItem(path='good/create', name='AppCreateGood', component='/app/good/createForm/index', meta=RouteMeta(title='创建货物', hidden=True)),
                                           RouteItem(path='good/edit', name='AppEditGood', component='/app/good/editForm/index', meta=RouteMeta(title='编辑货物', hidden=True)),
                                        #    RouteItem(path='issue', name='AppIssue', component='/app/issue/index', meta=RouteMeta(title='纠纷管理'))
                                           ]))
    router_list.append(RouteItem(path='/payment', name='payment', component='LAYOUT', meta=RouteMeta(title='支付管理', icon='money-circle'),
                                 children=[RouteItem(path='wallet', name='PaymentWallet', component='/payment/wallet/index', meta=RouteMeta(title='钱包管理')),
                                           RouteItem(path='order', name='PaymentOrder', component='/payment/order/index', meta=RouteMeta(title='订单管理')),
                                           ]))
    
    router_list.append(RouteItem(path='/chatting', name='chatting', component='LAYOUT', meta=RouteMeta(title='聊天管理', icon='chat'),
                                 children=[RouteItem(path='demo', name='ChattingDemo', component='/chatting/demo/index', meta=RouteMeta(title='聊天测试页面')),
                                           RouteItem(path='ChatView', name='ChatManager', component='/chatting/ChatView/index', meta=RouteMeta(title='聊天管理页面'))
                                           ]))
    
    if user_info.level == 'superuser':
        router_list.append(RouteItem(path='/setting', name='setting', component='LAYOUT', meta=RouteMeta(title='系统设置', icon='setting'),
                                    children=[RouteItem(path='admin', name='SettingAdmin', component='/setting/admin/index', meta=RouteMeta(title='管理员设置')),
                                              RouteItem(path='admin/edit', name='AdminEdit', component='/setting/admin/editForm/index', meta=RouteMeta(title='编辑管理员信息', hidden=True)),
                                              RouteItem(path='admin/create', name='AdminCreate', component='/setting/admin/createForm/index', meta=RouteMeta(title='创建管理员', hidden=True)),
                                            # RouteItem(path='log', name='SettingLog', component='setting/log/index', meta=RouteMeta(title='日志管理'))
                                            ]))

    return BaseResponse(data={'list':  [json.loads(jsonpickle.encode(i, unpicklable=False)) for i in router_list]}).dict()



@api.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_info():
    # to-do
    # use redis to cache last period data then calculate the increasing/decreasing rating.
    
    # get url from env
    chat_service_url = os.environ.get('CHAT_SERVICE_URL', 'http://localhost:5000') + '/dev/clients'
    try:
        response = requests.request("GET", chat_service_url)
        user_online = response.json()['data']['count']
    except:
        user_online = -1
    
    # get total user count
    total_user_num = User.query.count()
    
    # get total good count
    total_good_num = Good.query.count()
    
    # get total good pending for censor
    total_good_pending_num = Good.query.filter_by(state=Good.GOOD_STATES_ENUM[0]).count()
    
    # get all dashboard panel info
    DashboardPanelList = []
    DashboardPanelList.append(DashboardPanel(title='用户总数', number=total_user_num, leftType='icon-user', route='/app/user'))
    DashboardPanelList.append(DashboardPanel(title='在线用户', number=user_online, leftType='icon-bar', route='/chat/manager'))
    DashboardPanelList.append(DashboardPanel(title='货物总数', number=total_good_num, leftType='icon-control-platform', route='/app/good'))
    DashboardPanelList.append(DashboardPanel(title='待审核货物', number=total_good_pending_num, leftType='icon-layers', route='/censor/good'))
    
    return BaseResponse(data={'list':  json.loads(jsonpickle.encode(DashboardPanelList, unpicklable=False))}).dict()



@api.route('/hello', methods=['GET'])
def hello():
    return 'hello world'