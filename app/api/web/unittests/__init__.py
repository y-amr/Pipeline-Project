from flask import Blueprint

web_unittests_api = Blueprint('web_unittests_api', __name__)

from . import unit_tests