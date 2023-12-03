import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask import Flask
from app import create_app, db
from flask_cors import CORS
import click
from gevent import pywsgi
app = create_app('production')
# CORS(app=app, supports_credentials=True)
    
# @app.cli.command()
# def test():
#     """Runs the unit tests."""
#     import sys
#     import unittest

#     tests = unittest.TestLoader().discover("tests")
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.errors or result.failures:
#         sys.exit(1)

@app.cli.command()
def clean_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


@app.cli.command()
def fill_db():
    from utils.db_generator import FakeGenerator
    FakeGenerator().start(count=1000)


if __name__ == '__main__':
    
    # from app.api.auth.models import AdminUser
    # from app.api.users.models import User
    # from utils.db_generator import FakeGenerator
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #     FakeGenerator().start()

    server = pywsgi.WSGIServer(('0.0.0.0', 3001), app)
    server.serve_forever()
    # Flask.run(app, host='0.0.0.0', port=int(os.environ.get('FLASK_PORT', '3000')))