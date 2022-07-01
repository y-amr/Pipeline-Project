from flask import render_template, request, session
from app import app
from app.authentication import requires_auth
from . import web_parameters_api
from ...model.objects.parameter import Parameter
from ...model.services.parameter_service import ParameterService


class ParametersForm:
    USER_COUNTRY_CODE = 'USER_COUNTRY_CODE'
    USER_PARTY_ID = 'USER_PARTY_ID'
    SERVER_COUNTRY_CODE = 'SERVER_COUNTRY_CODE'
    SERVER_PARTY_ID = 'SERVER_PARTY_ID'
    ENDPOINT = 'ENDPOINT'
    AUTHORISATION_TOKEN_FROMSERVER = 'AUTHORISATION_TOKEN_FROMSERVER'
    AUTHORISATION_TOKEN_TOSERVER = 'AUTHORISATION_TOKEN_TOSERVER'
    ENDPOINT_211_CPO_TOKENS = 'ENDPOINT_211_CPO_TOKENS'
    ENDPOINT_211_CPO_COMMANDS = 'ENDPOINT_211_CPO_COMMANDS'
    ENDPOINT_211_CPO_LOCATIONS = 'ENDPOINT_211_CPO_LOCATIONS'
    ENDPOINT_211_CPO_CDRS = 'ENDPOINT_211_CPO_CDRS'
    ENDPOINT_211_CPO_SESSIONS = 'ENDPOINT_211_CPO_SESSIONS'
    ENDPOINT_211_CPO_VERSIONS = 'ENDPOINT_211_CPO_VERSIONS'
    ENDPOINT_211_CPO_CREDENTIALS = 'ENDPOINT_211_CPO_CREDENTIALS'
    ENDPOINT_211_CPO_TARIFFS = 'ENDPOINT_211_CPO_TARIFFS'
    ENDPOINT_211_EMSP_TOKENS = 'ENDPOINT_211_EMSP_TOKENS'
    ENDPOINT_211_EMSP_COMMANDS = 'ENDPOINT_211_EMSP_COMMANDS'
    ENDPOINT_211_EMSP_LOCATIONS = 'ENDPOINT_211_EMSP_LOCATIONS'
    ENDPOINT_211_EMSP_CDRS = 'ENDPOINT_211_EMSP_CDRS'
    ENDPOINT_211_EMSP_SESSIONS = 'ENDPOINT_211_EMSP_SESSIONS'
    ENDPOINT_211_EMSP_VERSIONS = 'ENDPOINT_211_EMSP_VERSIONS'
    ENDPOINT_211_EMSP_CREDENTIALS = 'ENDPOINT_211_EMSP_CREDENTIALS'
    ENDPOINT_211_EMSP_TARIFFS = 'ENDPOINT_211_EMSP_TARIFFS'


@web_parameters_api.route("", methods=['GET', 'POST'])
@requires_auth
def get_parameters():
    if request.method == 'GET':
        params = ParameterService.get_all_parameters_by_userid(session['profile']['user_id'])
        parametersForm = ParametersForm()
        return render_template("parameters/index.html", title='Parameters', parameters=params,
                               parametersForm=parametersForm, version=app.config['VERSION'])
    elif request.method == 'POST':
        parameter_list = []
        for fieldnames, value in request.form.items():
            if value is not '':
                parameter_list.append(Parameter(key=fieldnames, value=value, user_id=session['profile']['user_id']))
        ParameterService.save_parameters(parameter_list)
        params = ParameterService.get_all_parameters_by_userid(session['profile']['user_id'])
        parametersForm = ParametersForm()
        return render_template("parameters/index.html", title='Parameters', parameters=params,
                               parametersForm=parametersForm, version=app.config['VERSION'])
