from flask import Blueprint

web_parameters_api = Blueprint('web_parameters_api', __name__)

from . import parameters
