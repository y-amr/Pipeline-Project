from flask import render_template
from app import app
from app.api.client.two_one_one.cpo import fromserver_cpo_211
from app.api.client.two_one_one.emsp import fromserver_emsp_211
from app.api.server.two_one_one.cpo import ocpi_cpo_211
from app.api.server.two_one_one.emsp import ocpi_emsp_211
from app.api.server.versions import ocpi_emsp_versions, ocpi_cpo_versions
from app.api.web import web_api
from app.api.web.parameters import web_parameters_api
from app.api.web.unittests import web_unittests_api
from app.api.web.non_reg import web_non_reg_api
from app.authentication import requires_auth


@app.route("/")
@requires_auth
def home():
    return render_template("homepage.html", title="GIREVE Testing Platform", version=app.config['VERSION'])


# Blueprint API
app.register_blueprint(ocpi_cpo_211, url_prefix='/ocpi/cpo/2.1.1')
app.register_blueprint(ocpi_emsp_211, url_prefix='/ocpi/emsp/2.1.1')
app.register_blueprint(web_api, url_prefix='/local_api')
app.register_blueprint(web_parameters_api, url_prefix='/web/parameters')
app.register_blueprint(web_unittests_api, url_prefix='/web/unit-tests')
app.register_blueprint(fromserver_cpo_211, url_prefix='/fromserver/ocpi/cpo/2.1.1')
app.register_blueprint(fromserver_emsp_211, url_prefix='/fromserver/ocpi/emsp/2.1.1')
app.register_blueprint(ocpi_emsp_versions, url_prefix='/ocpi/emsp')
app.register_blueprint(ocpi_cpo_versions, url_prefix='/ocpi/cpo')
app.register_blueprint(web_non_reg_api, url_prefix='/web/non_reg')

