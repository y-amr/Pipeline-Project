from flask import Blueprint

ocpi_cpo_211 = Blueprint('ocpi_cpo_211', __name__)

from . import toserver_cpo_tokens, versions, toserver_cpo_locations, toserver_cpo_sessions, toserver_cpo_cdrs, toserver_cpo_tariffs, toserver_cpo_commands, toserver_cpo_versions, toserver_cpo_credentials
