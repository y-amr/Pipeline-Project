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
from app.api.utils.two_one_one.objects.locations_object import Locations
from app.api.utils.two_one_one.objects.ocpi_response import OCPIResponse
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Test, Report
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.api.utils.two_one_one.validators.url_validator import URLValidator
from app.authentication import requires_auth_api


@ocpi_emsp_211.route("/locations/<country_code>/<party_id>/<location_id>", methods=['PUT'])
@requires_auth_api
def toserver_emsp_locations_put(country_code, party_id, location_id):
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
                                                                                  path_to_schema="app/api/utils/two_one_one/jsonschema/objects/OCPI_V211_Object_Locations.json")
        result_tab.extend(result_tab_req_body)
        if not result_bool_req_body:
            test_request.tests = result_tab
            # test_request = TestRequest(request.url, request.headers, request.json, result_tab)
            test_response.body = OCPIResponse.response_error(
                message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
                error_code=2000)
        elif location_id != test_request.body.get('id'):
            result_tab.append(Test(level=Test.ERROR, text="The 'id' in the payload doesn't match the one in the URL"))
            test_request.tests = result_tab
            test_response.body = OCPIResponse.response_error(
                message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
                error_code=2000)
        else:
            # Success
            test_request.tests = result_tab
            # test_request = TestRequest(request.url, request.headers, request.json, result_tab)
            ocpi_response = OCPIResponse(data=None)
            test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                                message=','.join(v.__str__() for v in result_tab))

    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one, name=IOPWebservice.WS_NAME_PUT_emsp_Locations, ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize, status=test_report.get_status(test_report.request), web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    return make_response(test_response.body, test_response.http_status_code)


@ocpi_emsp_211.route("/locations/<country_code>/<party_id>/<location_id>", methods=['PATCH'])
@requires_auth_api
def toserver_emsp_locations_patch(country_code, party_id, location_id):
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
                                                                                  path_to_schema="app/api/utils/two_one_one/jsonschema/flows/locations/OCPI_V211_ToServer_patch_emsp_locations.json")
        result_tab.extend(result_tab_req_body)
        if not result_bool_req_body:
            test_request.tests = result_tab
            # test_request = TestRequest(request.url, request.headers, request.json, result_tab)
            test_response.body = OCPIResponse.response_error(
                message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
                error_code=2000)
        elif test_request.body.get('id') is not None and location_id != test_request.body.get('id'):
            result_tab.append(
                Test(level=Test.ERROR, text="The 'id' in the payload doesn't match the one in the URL"))
            test_request.tests = result_tab
            test_response.body = OCPIResponse.response_error(
                message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
                error_code=2000)
        else:
            # Success
            test_request.tests = result_tab
            # test_request = TestRequest(request.url, request.headers, request.json, result_tab)
            ocpi_response = OCPIResponse(data=None)
            test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                                message=','.join(v.__str__() for v in result_tab))

    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_PATCH_emsp_Locations,
                                                                              ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.request),
                                                  web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    return make_response(test_response.body, test_response.http_status_code)


@ocpi_emsp_211.route("/locations/<country_code>/<party_id>/<location_id>", methods=['GET'])
@requires_auth_api
def toserver_emsp_locations_get(country_code, party_id, location_id):
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
        get_locations_found_parameter = ParameterService.get_parameters_by_key_userid(Parameter.GET_LOCATIONS_FOUND, g.user_id)
        # if Server must return not found error
        if get_locations_found_parameter is not None and get_locations_found_parameter.value == Constants.NO_CONSTANT:
            test_response.http_status_code = status.HTTP_404_NOT_FOUND
            ocpi_response = OCPIResponse(data=None)
        else:
            lct = Locations(location_id=location_id, country_code=country_code, party_id=party_id)
            ocpi_response = OCPIResponse(data=lct.serialize)
        test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                            message=','.join(v.__str__() for v in result_tab))

    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one, name=IOPWebservice.WS_NAME_GET_emsp_Locations, ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize, status=test_report.get_status(test_report.request), web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    return make_response(test_response.body, test_response.http_status_code)


@ocpi_emsp_211.route("/locations<wildcard:path>", methods=['PATCH', 'PUT', 'DELETE', 'GET', 'POST'])
def toserver_emsp_locations_error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return make_response("It is not an OCPI Webservice", 400)
