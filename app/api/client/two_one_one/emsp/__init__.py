from flask import Blueprint

fromserver_emsp_211 = Blueprint('fromserver_emsp_211', __name__)

from . import fromserver_emsp_tokens, fromserver_emsp_locations, fromserver_emsp_sessions, fromserver_emsp_cdrs, fromserver_emsp_tariffs, fromserver_emsp_commands, fromserver_emsp_versions, fromserver_emsp_credentials
