import logging

from flask import make_response, request, g
from flask_api import status
from sqlalchemy import func

from app.api.model.objects.iop_webservice import IOPWebservice
from app.api.model.objects.ocpi_version import OCPIVersion
from app.api.model.objects.test_report import TestReport
from app.api.model.services.iop_webservice_service import IOPWebserviceService
from app.api.model.services.test_report_service import TestReportService
from app.api.server.two_one_one.emsp import ocpi_emsp_211
from app.api.utils.two_one_one.objects.ocpi_response import OCPIResponse
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Report
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.authentication import requires_auth_api


@ocpi_emsp_211.route("/commands/<session_id>", methods=['POST'])
@requires_auth_api
def toserver_emsp_commands_callback_post(session_id):
    # Init result table
    result_tab = []
    test_request = TestRequest(url=request.url, headers=request.headers, body=request.json, tests=None)
    test_response = TestResponse(headers=None, tests=None, body=None, http_status_code=status.HTTP_200_OK)

    # Test des headers
    request_headers = HeadersValidator(request.headers)
    result_bool_req_headers, result_tab_req_headers = request_headers.standard_validation(g.user_id)
    result_tab.extend(result_tab_req_headers)

    # If error on the header or on the URL
    if not result_bool_req_headers:
        test_request.tests = result_tab
        test_response.body = OCPIResponse.response_error(
            message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
            error_code=2000)
    else:
        # Test de la payload
        request_body = BodyValidator(test_request.body)
        result_bool_req_body, result_tab_req_body = request_body.schema_validator(self=request_body,
                                                                                  path_to_schema="app/api/utils/two_one_one/jsonschema/flows/commands/OCPI_V211_ToServer_post_emsp_commands-callback.json")
        result_tab.extend(result_tab_req_body)
        if not result_bool_req_body:
            test_request.tests = result_tab
            test_response.body = OCPIResponse.response_error(
                message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
                error_code=2000)
        else:
            # Success
            test_request.tests = result_tab
            ocpi_response = OCPIResponse(data=None)
            test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                                message=','.join(v.__str__() for v in result_tab))

    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_POST_emsp_Commands_CALLBACK,
                                                                              ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.request),
                                                  web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    return make_response(test_response.body, test_response.http_status_code)


@ocpi_emsp_211.route("/commands<wildcard:path>", methods=['PATCH', 'PUT', 'DELETE', 'GET', 'POST'])
def toserver_emsp_commands_error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return make_response("It is not an OCPI Webservice", 400)
