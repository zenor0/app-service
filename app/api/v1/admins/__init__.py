from flask import Blueprint

admins = Blueprint("admins", __name__)

from . import views


