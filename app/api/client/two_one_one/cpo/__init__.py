from flask import Blueprint

fromserver_cpo_211 = Blueprint('fromserver_cpo_211', __name__)

from . import fromserver_cpo_tokens, fromserver_cpo_locations, fromserver_cpo_sessions, fromserver_cpo_cdrs, fromserver_cpo_tariffs, fromserver_cpo_commands, fromserver_cpo_versions, fromserver_cpo_credentials
