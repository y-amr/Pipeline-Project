import logging
import os
from logging.config import dictConfig
from pathlib import Path
from decouple import config

# init du logger
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})
# Supprime les logs inutiles dans la console
log = logging.getLogger('werkzeug')
log.level = logging.DEBUG


class Config(object):
    VERSION = open("./version.txt", 'r').read()
    SESSION_TYPE = 'filesystem'
    BOOTSTRAP_SERVE_LOCAL = 'true'
    SECRET_KEY = config('SECRET_KEY')
    SERVER_PORT = config('SERVER_PORT')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Path().absolute(), 'girevetest.sqlite')
    SQLALCHEMY_DATABASE_SERVER = config('SQLALCHEMY_DATABASE_SERVER')
    SQLALCHEMY_DATABASE_USER = config('SQLALCHEMY_DATABASE_USER')
    SQLALCHEMY_DATABASE_PASSWORD = config('SQLALCHEMY_DATABASE_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + SQLALCHEMY_DATABASE_USER + ':' + SQLALCHEMY_DATABASE_PASSWORD + '@' + SQLALCHEMY_DATABASE_SERVER + '/ocpi_tester'
    AUTH0_CLIENT_ID = config('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = config('AUTH0_CLIENT_SECRET')
    AUTH0_API_BASE_URL = config('AUTH0_API_BASE_URL')
    AUTH0_REDIRECT_URL = config('AUTH0_REDIRECT_URL')
    AUTH0_AUDIENCE = config('AUTH0_AUDIENCE')
    SERVER_URL = config('SERVER_URL')
    MAX_TEST_REPORT_DISPLAY = config('MAX_TEST_REPORT_DISPLAY')
