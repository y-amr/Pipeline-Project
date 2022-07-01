from flask import Blueprint

web_non_reg_api = Blueprint('web_non_reg_api', __name__)

from . import non_reg
