from flask import Blueprint

web_api = Blueprint('web_api', __name__)

from . import fromserver