from flask import Blueprint

carts = Blueprint("carts", __name__)

from . import views, models
