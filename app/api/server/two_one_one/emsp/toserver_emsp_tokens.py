import logging

from flask import make_response, request, g
from flask_api import status
from sqlalchemy import func

from app.api.model.objects.iop_webservice import IOPWebservice
from app.api.model.objects.ocpi_version import OCPIVersion
from app.api.model.objects.parameter import Parameter
from app.api.model.objects.test_report import TestReport
from app.api.model.services.iop_webservice_service import IOPWebserviceService
from app.api.model.services.parameter_service import ParameterService
from app.api.model.services.test_report_service import TestReportService
from app.api.utils.two_one_one.constants import Constants
from app.api.utils.two_one_one.helper import Helper
from app.api.utils.two_one_one.objects.ocpi_response import OCPIResponse
from app.api.utils.two_one_one.objects.pagination_parameters import PaginationParameters
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Report, Test
from app.api.utils.two_one_one.objects.tokens_object import Tokens
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.api.utils.two_one_one.validators.url_validator import URLValidator
from app.authentication import requires_auth_api
from . import ocpi_emsp_211


@ocpi_emsp_211.route("/tokens", methods=['GET'])
@requires_auth_api
def toserver_get_emsp_tokens():
    # Init result table
    result_tab = []
    test_request = TestRequest(url=request.url, headers=request.headers, body=request.json, tests=None)
    test_response = TestResponse(headers=None, tests=None, body=None, http_status_code=status.HTTP_200_OK)

    # Test de l'URL
    pagination_param = PaginationParameters(request=request)
    request_url = URLValidator(request.url)
    result_bool_req_url, result_tab_req_url = request_url.pagination_validation(pagination_param)
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
        param_get_max_limit = ParameterService.get_parameters_by_key_userid(Parameter.GET_MAX_LIMIT, g.user_id)
        if param_get_max_limit is None:
            param_get_max_limit = Constants.DEFAULT_GET_MAX_LIMIT_CONSTANT
        else:
            param_get_max_limit = int(param_get_max_limit.value)
        param_get_number_items_returned = ParameterService.get_parameters_by_key_userid(
            Parameter.GET_NUMBER_ITEMS_RETURNED, g.user_id)
        if param_get_number_items_returned is None:
            param_get_number_items_returned = Constants.DEFAULT_GET_NUMBER_ITEMS_RETURNED_CONSTANT
        else:
            param_get_number_items_returned = int(param_get_number_items_returned.value)
        limit = param_get_max_limit if pagination_param.limit is None or int(
            pagination_param.limit) > param_get_max_limit else int(pagination_param.limit)
        offset = 0 if pagination_param.offset is None else int(pagination_param.offset)
        tokens_to_return = []
        for i in range(limit):
            if offset + i < param_get_number_items_returned:
                tokens_to_return.append(Tokens(uid=1000 + offset + i))
        ocpi_response = OCPIResponse(data=tokens_to_return)
        test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                            message=','.join(v.__str__() for v in result_tab))
        # Build the header
        test_response.add_pagination_headers(self=test_response, base_url=request.base_url, req_limit=limit,
                                             offset=offset,
                                             pagination_param=pagination_param,
                                             total_count=param_get_number_items_returned, max_limit=param_get_max_limit)

    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_GET_emsp_Tokens,
                                                                              ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.request),
                                                  web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    response = make_response(test_response.body, test_response.http_status_code)
    if test_response.headers is not None:
        response.headers.update(test_response.headers)
    return response


@ocpi_emsp_211.route("/tokens/<token_uid>/authorize", methods=['POST'])
@requires_auth_api
def toserver_post_emsp_tokens_authorize(token_uid):
    # Init result table
    result_tab = []
    test_request = TestRequest(url=request.url, headers=request.headers, body=request.json, tests=None)
    test_response = TestResponse(headers=None, tests=None, body=None, http_status_code=status.HTTP_200_OK)
    # Test de l'URL
    result_bool_req_url = True
    if request.args.get(Constants.TYPE_CONSTANT) is not None and request.args.get(
            Constants.TYPE_CONSTANT) not in Tokens.TOKENS_TOKENSTYPE:
        result_tab.append(Test(level=Test.ERROR,
                               text="'type' property is not one of " + Tokens.TOKENS_TOKENSTYPE.__str__()))
        result_bool_req_url = False
    # Test des headers
    request_headers = HeadersValidator(request.headers)
    result_bool_req_headers, result_tab_req_headers = request_headers.standard_validation(g.user_id)
    result_tab.extend(result_tab_req_headers)
    result_bool_req_headers_ct_type, result_tab_req_headers_ct_type = request_headers.content_type_json_validation()
    result_tab.extend(result_tab_req_headers_ct_type)
    # Test du body
    request_body = BodyValidator(test_request.body)
    result_bool_req_body, result_tab_req_body = request_body.schema_validator(self=request_body,
                                                                              path_to_schema="app/api/utils/two_one_one/jsonschema/flows/tokens/OCPI_V211_ToServer_post_emsp_tokens-authorize.json")
    result_tab.extend(result_tab_req_body)
    # If error on the header or on the URL or on the body
    if not result_bool_req_url or not result_bool_req_headers or not result_bool_req_headers_ct_type or not result_bool_req_body:
        test_request.tests = result_tab
        test_response.body = OCPIResponse.response_error(
            message="Some errors occurred => " + ','.join(v.__str__() for v in result_tab),
            error_code=2000)
    else:
        # Build the response
        authorizationinfo_to_return = {}
        authorizationinfo_to_return = {'allowed': (
            ParameterService.get_parameters_by_key_userid(Parameter.POST_TOKEN_AUTHORIZE_ALLOWED,
                                                          g.user_id).value if ParameterService.get_parameters_by_key_userid(
                Parameter.POST_TOKEN_AUTHORIZE_ALLOWED, g.user_id) is not None else Constants.ALLOWED_CONSTANT)}
        if test_request.body is not None and test_request.body.get("location_id") is not None and \
                authorizationinfo_to_return['allowed'] == Constants.ALLOWED_CONSTANT:
            location_ref_to_return = test_request.body
            authorizationinfo_to_return['location'] = location_ref_to_return
        authorizationinfo_to_return['info'] = Helper.return_standard_ocpi_211_display_text()
        ocpi_response = OCPIResponse(data=authorizationinfo_to_return)
        test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                            message=','.join(v.__str__() for v in result_tab))
    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_POST_emsp_Tokens_authorize,
                                                                              ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.request),
                                                  web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    response = make_response(test_response.body, test_response.http_status_code)
    # response.headers
    return response


@ocpi_emsp_211.route("/tokens<wildcard:path>", methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
@requires_auth_api
def error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return make_response("It is not an OCPI Webservice", 400)
