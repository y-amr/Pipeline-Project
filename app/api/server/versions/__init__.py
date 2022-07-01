from flask import Blueprint

ocpi_emsp_versions = Blueprint('ocpi_emsp_versions', __name__)
ocpi_cpo_versions = Blueprint('ocpi_cpo_versions', __name__)

from . import toserver_versions
