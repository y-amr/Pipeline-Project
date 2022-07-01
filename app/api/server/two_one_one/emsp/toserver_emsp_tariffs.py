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
from app.api.utils.two_one_one.objects.ocpi_response import OCPIResponse
from app.api.utils.two_one_one.objects.tariffs_object import Tariffs
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Test, Report
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.api.utils.two_one_one.validators.url_validator import URLValidator
from app.authentication import requires_auth_api


@ocpi_emsp_211.route("/tariffs/<country_code>/<party_id>/<tariff_id>", methods=['PUT'])
@requires_auth_api
def toserver_emsp_tariffs_put(country_code, party_id, tariff_id):
    # Init result table
    result_tab = []
    test_request = TestRequest(url=request.url, headers=request.headers, body=request.json, tests=None)
    test_response = TestResponse(headers=None, tests=None, body=None, http_status_code=status.HTTP_200_OK)

    # Test de l'URL
    request_url = URLValidator(request.path)
    result_bool_req_url, result_tab_req_url = request_url.object_owner_validation(country_code, party_id, g.user_id)
    result_tab.extend(result_tab_req_url)

    # Test des headers
    request_headers = HeadersValidator(request.headers)
    result_bool_req_headers, result_tab_req_headers = request_headers.standard_validation(g.user_id)
    result_tab.extend(result_tab_req_headers)

    # If error on the header or on the URL
    if not result_bool_req_url or not result_bool_req_headers:
        test_request.tests = result_tab
        # test_request = TestRequest(request.url, request.headers, request.json, result_tab)
        test_response.body = OCPIResponse.response_error(
            message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
            error_code=2000)
    else:
        # Test de la payload
        request_body = BodyValidator(test_request.body)
        result_bool_req_body, result_tab_req_body = request_body.schema_validator(self=request_body,
                                                                                  path_to_schema="app/api/utils/two_one_one/jsonschema/objects/OCPI_V211_Object_Tariffs.json")
        result_tab.extend(result_tab_req_body)
        if not result_bool_req_body:
            test_request.tests = result_tab
            # test_request = TestRequest(request.url, request.headers, request.json, result_tab)
            test_response.body = OCPIResponse.response_error(
                message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
                error_code=2000)
        elif tariff_id != test_request.body.get('id'):
            result_tab.append(Test(level=Test.ERROR, text="The 'id' in the payload doesn't match the one in the URL"))
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
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one, name=IOPWebservice.WS_NAME_PUT_emsp_Tariffs, ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize, status=test_report.get_status(test_report.request), web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    return make_response(test_response.body, test_response.http_status_code)


@ocpi_emsp_211.route("/tariffs/<country_code>/<party_id>/<tariff_id>", methods=['PATCH'])
@requires_auth_api
def toserver_emsp_tariffs_patch(country_code, party_id, tariff_id):
    # Init result table
    result_tab = []
    test_request = TestRequest(url=request.url, headers=request.headers, body=request.json, tests=None)
    test_response = TestResponse(headers=None, tests=None, body=None, http_status_code=status.HTTP_200_OK)

    # Test de l'URL
    request_url = URLValidator(request.path)
    result_bool_req_url, result_tab_req_url = request_url.object_owner_validation(country_code, party_id, g.user_id)
    result_tab.extend(result_tab_req_url)

    # Test des headers
    request_headers = HeadersValidator(request.headers)
    result_bool_req_headers, result_tab_req_headers = request_headers.standard_validation(g.user_id)
    result_tab.extend(result_tab_req_headers)

    # If error on the header or on the URL
    if not result_bool_req_url or not result_bool_req_headers:
        test_request.tests = result_tab
        # test_request = TestRequest(request.url, request.headers, request.json, result_tab)
        test_response.body = OCPIResponse.response_error(
            message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
            error_code=2000)
    else:
        # Test de la payload
        request_body = BodyValidator(test_request.body)
        result_bool_req_body, result_tab_req_body = request_body.schema_validator(self=request_body,
                                                                                  path_to_schema="app/api/utils/two_one_one/jsonschema/flows/tariffs/OCPI_V211_ToServer_patch_emsp_tariffs.json")
        result_tab.extend(result_tab_req_body)
        if not result_bool_req_body:
            test_request.tests = result_tab
            # test_request = TestRequest(request.url, request.headers, request.json, result_tab)
            test_response.body = OCPIResponse.response_error(
                message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
                error_code=2000)
        elif test_request.body.get('id') is not None and tariff_id != test_request.body.get('id'):
            result_tab.append(
                Test(level=Test.ERROR, text="The 'id' in the payload doesn't match the one in the URL"))
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
                                                                              name=IOPWebservice.WS_NAME_PATCH_emsp_Tariffs,
                                                                              ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.request),
                                                  web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    return make_response(test_response.body, test_response.http_status_code)


@ocpi_emsp_211.route("/tariffs/<country_code>/<party_id>/<tariff_id>", methods=['GET'])
@requires_auth_api
def toserver_emsp_tariffs_get(country_code, party_id, tariff_id):
    # Init result table
    result_tab = []
    test_request = TestRequest(url=request.url, headers=request.headers, body=request.json, tests=None)
    test_response = TestResponse(headers=None, tests=None, body=None, http_status_code=status.HTTP_200_OK)

    # Test de l'URL
    request_url = URLValidator(request.path)
    result_bool_req_url, result_tab_req_url = request_url.object_owner_validation(country_code, party_id, g.user_id)
    result_tab.extend(result_tab_req_url)

    # Test des headers
    request_headers = HeadersValidator(request.headers)
    result_bool_req_headers, result_tab_req_headers = request_headers.standard_validation(g.user_id)
    result_tab.extend(result_tab_req_headers)
    result_bool_req_headers_ct_type, result_tab_req_headers_ct_type = request_headers.no_content_type_validation()
    result_tab.extend(result_tab_req_headers_ct_type)

    # If error on the header or on the URL
    if not result_bool_req_url or not result_bool_req_headers or not result_bool_req_headers_ct_type:
        test_request.tests = result_tab
        test_response.body = OCPIResponse.response_error(
            message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
            error_code=2000)
    else:
        # Build the response
        ocpi_response = None
        get_tariffs_found_parameter = ParameterService.get_parameters_by_key_userid(Parameter.GET_TARIFFS_FOUND, g.user_id)
        # if Server must return not found error
        if get_tariffs_found_parameter is not None and get_tariffs_found_parameter.value == Constants.NO_CONSTANT:
            test_response.http_status_code = status.HTTP_404_NOT_FOUND
            ocpi_response = OCPIResponse(data=None)
        else:
            trf = Tariffs(tariff_id=tariff_id)
            ocpi_response = OCPIResponse(data=trf.serialize)
        test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                            message=','.join(v.__str__() for v in result_tab))

    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one, name=IOPWebservice.WS_NAME_GET_emsp_Tariffs, ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize, status=test_report.get_status(test_report.request), web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    return make_response(test_response.body, test_response.http_status_code)


@ocpi_emsp_211.route("/tariffs/<country_code>/<party_id>/<tariff_id>", methods=['DELETE'])
@requires_auth_api
def toserver_emsp_tariffs_delete(country_code, party_id, tariff_id):
    # Init result table
    result_tab = []
    test_request = TestRequest(url=request.url, headers=request.headers, body=request.json, tests=None)
    test_response = TestResponse(headers=None, tests=None, body=None, http_status_code=status.HTTP_200_OK)

    # Test de l'URL
    request_url = URLValidator(request.path)
    result_bool_req_url, result_tab_req_url = request_url.object_owner_validation(country_code, party_id, g.user_id)
    result_tab.extend(result_tab_req_url)

    # Test des headers
    request_headers = HeadersValidator(request.headers)
    result_bool_req_headers, result_tab_req_headers = request_headers.standard_validation(g.user_id)
    result_tab.extend(result_tab_req_headers)
    result_bool_req_headers_ct_type, result_tab_req_headers_ct_type = request_headers.no_content_type_validation()
    result_tab.extend(result_tab_req_headers_ct_type)

    # If error on the header or on the URL
    if not result_bool_req_url or not result_bool_req_headers or not result_bool_req_headers_ct_type:
        test_request.tests = result_tab
        test_response.body = OCPIResponse.response_error(
            message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
            error_code=2000)
    else:
        # Build the response
        ocpi_response = None
        del_tariffs_found_parameter = ParameterService.get_parameters_by_key_userid(Parameter.GET_TARIFFS_FOUND, g.user_id)
        # if Server must return not found error
        if del_tariffs_found_parameter is not None and del_tariffs_found_parameter.value == Constants.NO_CONSTANT:
            test_response.http_status_code = status.HTTP_404_NOT_FOUND
        ocpi_response = OCPIResponse(data=None)
        test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                            message=','.join(v.__str__() for v in result_tab))

    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one, name=IOPWebservice.WS_NAME_DELETE_emsp_Tariffs, ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize, status=test_report.get_status(test_report.request), web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    return make_response(test_response.body, test_response.http_status_code)


@ocpi_emsp_211.route("/tariffs<wildcard:path>", methods=['PATCH', 'PUT', 'DELETE', 'GET', 'POST'])
def toserver_emsp_tariffs_error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return make_response("It is not an OCPI Webservice", 400)
