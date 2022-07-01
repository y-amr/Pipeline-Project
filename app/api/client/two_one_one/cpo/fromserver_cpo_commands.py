import json
import logging

from flask import session, request
from sqlalchemy import func

from app.api.client.two_one_one.cpo import fromserver_cpo_211
from app.api.model.objects.iop_webservice import IOPWebservice
from app.api.model.objects.ocpi_version import OCPIVersion
from app.api.model.objects.test_report import TestReport
from app.api.model.services.iop_webservice_service import IOPWebserviceService
from app.api.model.services.test_report_service import TestReportService
from app.api.utils.two_one_one.constants import Constants
from app.api.utils.two_one_one.helper import Helper
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Report
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.api.utils.two_one_one.validators.http_status_code_validator import HttpStatusCodeValidator
from app.authentication import requires_auth


@fromserver_cpo_211.route("/commands/POST_emsp_commands-callback", methods=['POST'])
@requires_auth
def fromserver_post_emsp_commands_callback():
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
    test_request.add_fromserver_request_authorization_token_header(session_user_id)

    # Build the URL
    command_url = request.get_json().get("command_url")
    if not Helper.is_valid_url(command_url):
        return "Please define a valid URL"
    test_request.url = command_url

    # Build the body
    test_request.body = {"result": request.get_json().get("command_response")}

    # Send request then build response
    try:
        response = test_request.send_post_request()
    except Exception as e:
        logging.error("Error during request for user : " + session_user_id + " => " + e.args.__str__())
        return "Error during request =>" + e.args.__str__()

    test_response = TestResponse(headers=response.headers, tests=None, body=response.text,
                                 http_status_code=response.status_code)

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
                                                                                       path_to_schema="app/api/utils/two_one_one/jsonschema/response/OCPI_V211_FromServer_standard_response_no_data.json")
            result_tab.extend(result_tab_req_body)

    # Create test_report
    test_response.tests = result_tab
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_POST_emsp_Commands_CALLBACK,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.response),
                                                  web_service_id=iop_ws.webservice_id,
                                                  user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_cpo_211.route("/commands<wildcard:path>", methods=['PATCH', 'PUT', 'DELETE', 'GET', 'POST'])
@requires_auth
def fromserver_cpo_commands_error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return Constants.ERROR_CONSTANT
