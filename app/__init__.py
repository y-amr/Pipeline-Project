import mimetypes
import os
import sys
from datetime import datetime

from flask import Flask
from flask_bootstrap import Bootstrap
from werkzeug.routing import BaseConverter
from app.configuration import Config

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)
# Define configuration
app.url_map.strict_slashes = False
app.config.from_object(Config)


# Valeur MIME Type
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

# initialisation de bootstrap
bootstrap = Bootstrap(app)


# Add URL converter for blueprints
class WildcardConverter(BaseConverter):
    regex = r'.*?'
    weight = 200


app.url_map.converters['wildcard'] = WildcardConverter


@app.context_processor
def init_year():
    return dict(currentYear=datetime.now().year)


from app.Base import Base, engine, db_session
from app import routes
from app import authentication


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
