import json
import logging

from flask import session, request
from sqlalchemy import func

from app.api.client.two_one_one.emsp import fromserver_emsp_211
from app.api.model.objects.iop_webservice import IOPWebservice
from app.api.model.objects.ocpi_version import OCPIVersion
from app.api.model.objects.parameter import Parameter
from app.api.model.objects.test_report import TestReport
from app.api.model.services.iop_webservice_service import IOPWebserviceService
from app.api.model.services.parameter_service import ParameterService
from app.api.model.services.test_report_service import TestReportService
from app.api.utils.two_one_one.constants import Constants
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Report
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.api.utils.two_one_one.validators.http_status_code_validator import HttpStatusCodeValidator
from app.authentication import requires_auth


@fromserver_emsp_211.route("/commands/POST_cpo_Commands-START_SESSION", methods=['POST'])
@requires_auth
def fromserver_post_cpo_commands_start_session():
    session_user_id = session['profile'].get('user_id')
    # creation de la requete a envoyer
    # Init result table
    result_tab = []
    test_request = TestRequest(url=None, headers=None, body=None, tests=None)

    # Check if user parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_fromserver_request_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Add headers to the request
    test_request.add_fromserver_request_content_type_json_header()
    test_request.add_fromserver_request_authorization_token_header(session_user_id)
    # création du body a envoyer d'aprés les données rentrée par l'utilisateur
    try:
        test_request.body = json.loads(request.get_json().get("request_template"))
    except (ValueError, Exception):
        return "Please fill a json request"

    # GET the URL
    if ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT_211_CPO_COMMANDS, session_user_id):
        test_request.url = ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT_211_CPO_COMMANDS,
                                                                         session_user_id).value + Constants.SLASH_CONSTANT + Constants.START_SESSION_CONSTANT
    else:
        # If no specific endpoint was specified : BUILD the URL from ENDPOINT
        user_endpoint = ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT, session_user_id).value
        test_request.url = user_endpoint + Constants.TO_CPO_COMMANDS_211_ENDPOINT_CONSTANT + Constants.SLASH_CONSTANT + Constants.START_SESSION_CONSTANT

    # Send request then build response
    try:
        response = test_request.send_post_request()
    except Exception as e:
        logging.error("Error during request for user : " + session_user_id + " => " + e.args.__str__())
        return "Error during request =>" + e.args.__str__()

    test_response = TestResponse(headers=response.headers, tests=None, body=response.text,
                                 http_status_code=response.status_code)

    # Check du HTTP status code
    result_bool_http_status_code, result_tab_http_status_code = HttpStatusCodeValidator.http_status_success_validation(
        test_response.http_status_code)
    result_tab.extend(result_tab_http_status_code)
    # Check des headers
    response_headers = HeadersValidator(test_response.headers)
    result_bool_res_headers_ct_type, result_tab_res_headers_ct_type = response_headers.content_type_json_validation()
    result_tab.extend(result_tab_res_headers_ct_type)
    if result_bool_http_status_code and result_bool_res_headers_ct_type:
        # Check du body
        response_body = BodyValidator(test_response.body)
        result_bool_json_body, result_tab_json_body = response_body.is_json_body()
        result_tab.extend(result_tab_json_body)
        if result_bool_json_body:
            test_response.body = json.loads(test_response.body)
            response_body = BodyValidator(test_response.body)
            result_bool_req_body, result_tab_req_body = response_body.schema_validator(self=response_body,
                                                                                       path_to_schema="app/api/utils/two_one_one/jsonschema/response/commands/OCPI_V211_FromServer_post_cpo_commands_START_SESSION.json")
            result_tab.extend(result_tab_req_body)

    # Create test_report
    test_response.tests = result_tab
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_POST_cpo_Commands_START_SESSION,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.response),
                                                  web_service_id=iop_ws.webservice_id,
                                                  user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_emsp_211.route("/commands/POST_cpo_Commands-STOP_SESSION", methods=['POST'])
@requires_auth
def fromserver_post_cpo_commands_stop_session():
    session_user_id = session['profile'].get('user_id')
    # creation de la requete a envoyer
    # Init result table
    result_tab = []
    test_request = TestRequest(url=None, headers=None, body=None, tests=None)

    # Check if user parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_fromserver_request_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Add headers to the request
    test_request.add_fromserver_request_content_type_json_header()
    test_request.add_fromserver_request_authorization_token_header(session_user_id)
    # création du body a envoyer d'aprés les données rentrée par l'utilisateur
    try:
        test_request.body = json.loads(request.get_json().get("request_template"))
    except (ValueError, Exception):
        return "Please fill a json request"

    # GET the URL
    if ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT_211_CPO_COMMANDS, session_user_id):
        test_request.url = ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT_211_CPO_COMMANDS,
                                                                         session_user_id).value + Constants.SLASH_CONSTANT + Constants.STOP_SESSION_CONSTANT
    else:
        # If no specific endpoint was specified : BUILD the URL from ENDPOINT
        user_endpoint = ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT, session_user_id).value
        test_request.url = user_endpoint + Constants.TO_CPO_COMMANDS_211_ENDPOINT_CONSTANT + Constants.SLASH_CONSTANT + Constants.STOP_SESSION_CONSTANT

    # Send request then build response
    try:
        response = test_request.send_post_request()
    except Exception as e:
        logging.error("Error during request for user : " + session_user_id + " => " + e.args.__str__())
        return "Error during request =>" + e.args.__str__()

    test_response = TestResponse(headers=response.headers, tests=None, body=response.text,
                                 http_status_code=response.status_code)

    # Check du HTTP status code
    result_bool_http_status_code, result_tab_http_status_code = HttpStatusCodeValidator.http_status_success_validation(
        test_response.http_status_code)
    result_tab.extend(result_tab_http_status_code)
    # Check des headers
    response_headers = HeadersValidator(test_response.headers)
    result_bool_res_headers_ct_type, result_tab_res_headers_ct_type = response_headers.content_type_json_validation()
    result_tab.extend(result_tab_res_headers_ct_type)
    if result_bool_http_status_code and result_bool_res_headers_ct_type:
        # Check du body
        response_body = BodyValidator(test_response.body)
        result_bool_json_body, result_tab_json_body = response_body.is_json_body()
        result_tab.extend(result_tab_json_body)
        if result_bool_json_body:
            test_response.body = json.loads(test_response.body)
            response_body = BodyValidator(test_response.body)
            result_bool_req_body, result_tab_req_body = response_body.schema_validator(self=response_body,
                                                                                       path_to_schema="app/api/utils/two_one_one/jsonschema/response/commands/OCPI_V211_FromServer_post_cpo_commands_STOP_SESSION.json")
            result_tab.extend(result_tab_req_body)

    # Create test_report
    test_response.tests = result_tab
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_POST_cpo_Commands_STOP_SESSION,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.response),
                                                  web_service_id=iop_ws.webservice_id,
                                                  user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_emsp_211.route("/commands<wildcard:path>", methods=['PATCH', 'PUT', 'DELETE', 'GET', 'POST'])
@requires_auth
def fromserver_emsp_commands_error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return Constants.ERROR_CONSTANT
