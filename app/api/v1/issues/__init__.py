from flask import Blueprint

issues = Blueprint("issues", __name__)

from . import views, models
