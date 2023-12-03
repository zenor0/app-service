
from flask import Blueprint
# from . import auth, dev, users


api = Blueprint("api", __name__)

from .auth import auth as auth_blueprint
api.register_blueprint(auth_blueprint, url_prefix='/auth')

from .dev import dev as dev_blueprint
api.register_blueprint(dev_blueprint, url_prefix='/dev')

from .users import users as users_blueprint
api.register_blueprint(users_blueprint, url_prefix='/users')

from .goods import goods as goods_blueprint
api.register_blueprint(goods_blueprint, url_prefix='/goods')

from .admins import admins as admins_blueprint
api.register_blueprint(admins_blueprint, url_prefix='/admins')

from .wallets import wallets as wallets_blueprint
api.register_blueprint(wallets_blueprint, url_prefix='/wallets')

from .issues import issues as issues_blueprint
api.register_blueprint(issues_blueprint, url_prefix='/issues')

from .orders import orders as orders_blueprint
api.register_blueprint(orders_blueprint, url_prefix='/orders')


from . import views, models
