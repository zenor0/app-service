from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api
from config import config, Config

db = SQLAlchemy()

# app/__init__.py
def create_app(config_name):
    app = Flask(__name__)
    
    # load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # connect to db
    db.init_app(app)
    
    # set up JWT
    jwt = JWTManager(app)
    
    # register api routes
    from .api.v2 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    # app.register_blueprint(api_blueprint, url_prefix='/')
    
    # allow CORS
    CORS(app, origins="*", supports_credentials=True)
    return app
