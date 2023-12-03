import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
BASEDB = os.environ.get("DATABASE_BASE_URI")
APPBASEDB = os.environ.get("APP_DATABASE_BASE_URI")
DATABASE = os.environ.get("DATABASE")


def create_admin_sqlalchemy_uri(db_name):
    return BASEDB + db_name
    # return "sqlite:///" + os.path.join(BASEDIR, db_name)


def create_app_sqlalchemy_uri(db_name):
    return APPBASEDB + db_name


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret key, just for testing"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 36000
    JWT_SECRET = os.environ.get("SECRET_KEY") or 'testing'
    JWT_EXPIRY = 36000

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = create_admin_sqlalchemy_uri("admin_dev")
    SQLALCHEMY_BINDS = {
        'app': create_app_sqlalchemy_uri('app_dev'),
    }


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = create_admin_sqlalchemy_uri("admin_test")
    SQLALCHEMY_BINDS = {
        'app': create_app_sqlalchemy_uri('app_test'),
    }
    WTF_CSRF_ENABLED = False
    import logging

    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.DEBUG)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = create_admin_sqlalchemy_uri("xianju-app")

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
