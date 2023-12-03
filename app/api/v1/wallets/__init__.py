from flask import Blueprint

wallets = Blueprint("wallets", __name__)

from . import views, models
