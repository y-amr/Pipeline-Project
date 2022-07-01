import logging

from decouple import config
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
from app.api.server.two_one_one.cpo import ocpi_cpo_211
from app.api.utils.two_one_one.constants import Constants
from app.api.utils.two_one_one.objects.ocpi_response import OCPIResponse
from app.api.utils.two_one_one.objects.pagination_parameters import PaginationParameters
from app.api.utils.two_one_one.objects.sessions_object import Sessions
from app.api.utils.two_one_one.objects.tariffs_object import Tariffs
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Report
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.api.utils.two_one_one.validators.url_validator import URLValidator
from app.authentication import requires_auth_api


@ocpi_cpo_211.route("/tariffs", methods=['GET'])
@requires_auth_api
def toserver_get_cpo_tariffs():
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
        tariffs_to_return = []
        for i in range(limit):
            if offset + i < param_get_number_items_returned:
                tariffs_to_return.append(Tariffs(tariff_id=1000 + offset + i))
        ocpi_response = OCPIResponse(data=tariffs_to_return)
        test_response.body = ocpi_response.response_success(self=ocpi_response,
                                                            message=','.join(v.__str__() for v in result_tab))
        # Build the header
        base_url = config('SERVER_URL') + Constants.TO_CPO_TARIFFS_211_ENDPOINT_CONSTANT
        test_response.add_pagination_headers(self=test_response, base_url=base_url, req_limit=limit,
                                             offset=offset,
                                             pagination_param=pagination_param,
                                             total_count=param_get_number_items_returned, max_limit=param_get_max_limit)
        '''if param_get_number_items_returned > offset + limit:
            test_response.add_link_header(self=test_response, base_url=request.base_url, limit=limit, offset=offset,
                                          pagination_param=pagination_param)'''

    # Construction du test report
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_GET_cpo_Tariffs,
                                                                              ws_type=IOPWebservice.TYPE_TOSERVER)
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.request),
                                                  web_service_id=iop_ws.webservice_id, user_id=g.user_id))
    response = make_response(test_response.body, test_response.http_status_code)
    if test_response.headers is not None:
        response.headers.update(test_response.headers)
    return response


@ocpi_cpo_211.route("/tariffs<wildcard:path>", methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
@requires_auth_api
def toserver_cpo_tariffs_error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return make_response("It is not an OCPI Webservice", 400)
