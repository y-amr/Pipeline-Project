import logging

from flask import request, g, make_response
from flask_api import status
from sqlalchemy import func

from app.api.model.objects.iop_webservice import IOPWebservice
from app.api.model.objects.ocpi_version import OCPIVersion
from app.api.model.objects.parameter import Parameter
from app.api.model.objects.test_report import TestReport
from app.api.model.services.iop_webservice_service import IOPWebserviceService
from app.api.model.services.parameter_service import ParameterService
from app.api.model.services.test_report_service import TestReportService
from app.api.server.two_one_one.emsp import ocpi_emsp_211
from app.api.utils.two_one_one.constants import Constants
from app.api.utils.two_one_one.objects.credentials_object import Credentials
from app.api.utils.two_one_one.objects.ocpi_response import OCPIResponse
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Report
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.authentication import requires_auth_api


@ocpi_emsp_211.route("/credentials", methods=['POST'])
@requires_auth_api
def toserver_post_emsp_credentials():
    # Init result table
    result_tab = []
    test_request = TestRequest(url=request.url, headers=request.headers, body=request.json, tests=None)
    test_response = TestResponse(headers=None, tests=None, body=None, http_status_code=status.HTTP_200_OK)

    # Test des headers
    request_headers = HeadersValidator(request.headers)
    result_bool_req_headers, result_tab_req_headers = request_headers.standard_validation(g.user_id)
    result_tab.extend(result_tab_req_headers)
    result_bool_req_headers_ct_type, result_tab_req_headers_ct_type = request_headers.content_type_json_validation()
    result_tab.extend(result_tab_req_headers_ct_type)
    # Test du body
    request_body = BodyValidator(test_request.body)
    result_bool_req_body, result_tab_req_body = request_body.schema_validator(self=request_body,
                                                                              path_to_schema="app/api/utils/two_one_one/jsonschema/objects/OCPI_V211_Object_Credentials.json")
    result_tab.extend(result_tab_req_body)
    # If error on the header or on the URL or on the body
    if not result_bool_req_headers or not result_bool_req_headers_ct_type or not result_bool_req_body:
        test_request.tests = result_tab
        test_response.body = OCPIResponse.response_error(
            message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
            error_code=2000)
    else:
        # Build the response
        credentials_to_return = Credentials(country_code=ParameterService.get_parameters_by_key_userid(key_value=Parameter.SERVER_COUNTRY_CODE, user_id=g.user_id).value if ParameterService.get_parameters_by_key_userid(key_value=Parameter.SERVER_COUNTRY_CODE, user_id=g.user_id) is not None else 'FR', party_id=ParameterService.get_parameters_by_key_userid(key_value=Parameter.SERVER_PARTY_ID, user_id=g.user_id).value if ParameterService.get_parameters_by_key_userid(key_value=Parameter.SERVER_PARTY_ID, user_id=g.user_id) is not None else 'EMP', role=Constants.EMSP_CONSTANT)
        ocpi_response = OCPIResponse(data=credentials_to_return.serialize)
        test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                            message=','.join(v.__str__() for v in result_tab))
    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_POST_emsp_credentials,
                                                                              ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.request),
                                                  web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    response = make_response(test_response.body, test_response.http_status_code)
    return response


@ocpi_emsp_211.route("/credentials<wildcard:path>", methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
@requires_auth_api
def toserver_emsp_credentials_error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return make_response("It is not an OCPI Webservice", 400)
