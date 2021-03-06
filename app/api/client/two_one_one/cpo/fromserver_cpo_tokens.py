import json
import logging

from flask import request, session
from sqlalchemy import func

from app.api.client.two_one_one.cpo import fromserver_cpo_211
from app.api.model.objects.iop_webservice import IOPWebservice
from app.api.model.objects.ocpi_version import OCPIVersion
from app.api.model.objects.parameter import Parameter
from app.api.model.objects.test_report import TestReport
from app.api.model.services.iop_webservice_service import IOPWebserviceService
from app.api.model.services.parameter_service import ParameterService
from app.api.model.services.test_report_service import TestReportService
from app.api.utils.two_one_one.constants import Constants
from app.api.utils.two_one_one.objects.pagination_parameters import PaginationParameters
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Report
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.api.utils.two_one_one.validators.http_status_code_validator import HttpStatusCodeValidator
from app.api.utils.two_one_one.validators.url_validator import URLValidator
from app.authentication import requires_auth


@fromserver_cpo_211.route("/tokens/POST_emsp_Tokens-authorize", methods=['POST'])
@requires_auth
def fromserver_post_emsp_tokens_authorize(flag_ng=False, user_id="", non_regression_id="", use_cases_id="", nb_request="", request_data=""):
    if flag_ng:
        session_user_id = user_id
    else:
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
    # cr??ation du body a envoyer d'apr??s les donn??es rentr??e par l'utilisateur ( ou pour les data-test IOP)
    if flag_ng:
        data = request_data
    else:
        data = request.get_json()
    token_type = ''
    if data.get("token_type"):
        token_type = '?type=' + data.get("token_type")
    token_authorization = {}
    if data.get("token_uid"):
        token_uid = data.get("token_uid")
    else:
        token_uid = '11111'
    if data.get("location_id"):
        token_authorization["location_id"] = data.get("location_id")
    else:
        token_authorization["location_id"] = '1'
    if data.get("evse_id"):
        token_authorization["evse_uids"] = [data.get("evse_id")]
    else:
        token_authorization["evse_uids"] = ['1']
    if data.get("connector_id"):
        token_authorization["connector_ids"] = [data.get("connector_id")]
    test_request.body = token_authorization

    if ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT_211_EMSP_TOKENS, session_user_id):
        test_request.url = ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT_211_EMSP_TOKENS,
                                                                         session_user_id).value + Constants.SLASH_CONSTANT + token_uid + Constants.SLASH_AUTHORIZE_CONSTANT + token_type
    else:
        # If no specific endpoint was specified : BUILD the URL from ENDPOINT
        user_endpoint = ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT, session_user_id).value
        test_request.url = user_endpoint + Constants.TO_EMSP_TOKENS_211_ENDPOINT_CONSTANT + Constants.SLASH_CONSTANT + token_uid + Constants.SLASH_AUTHORIZE_CONSTANT + token_type


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
                                                                                       path_to_schema="app/api/utils/two_one_one/jsonschema/response/tokens/OCPI_V211_FromServer_post_emsp_tokens_authorize.json")
            result_tab.extend(result_tab_req_body)

    # Create test_report
    test_response.tests = result_tab
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_POST_emsp_Tokens_authorize,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    if flag_ng:
        # Enregistrement du rapport de test
        TestReportService.save_test_report_ng(NonRegressionReport(date_report=func.now(), report=test_report.serialize,
                                                                  non_regression_id=non_regression_id,
                                                                  use_cases_id=use_cases_id,
                                                                  nb_request=nb_request,
                                                                  status=test_report.get_status(test_report.response),
                                                                  web_service_id=iop_ws.webservice_id,
                                                                  user_id=session_user_id))

    else:
        # Enregistrement du rapport de test
        TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                      status=test_report.get_status(test_report.response),
                                                      web_service_id=iop_ws.webservice_id,
                                                      user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_cpo_211.route("/tokens/GET_emsp_Tokens", methods=['POST'])
@requires_auth
def fromserver_get_emsp_tokens():
    session_user_id = session['profile'].get('user_id')
    # creation de la requete a envoyer
    # Init result table
    result_tab = []
    test_request = TestRequest(url=None, headers=None, body=None, tests=None)

    # Check if user parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_fromserver_request_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Check if pagination parameters are valid
    data = request.get_json()
    pg_param = PaginationParameters(date_from=data.get('date_from'), date_to=data.get('date_to'),
                                    limit=data.get('limit'), offset=data.get('offset'))
    check_param_bool, check_param_mess = URLValidator.pagination_validation(pg_param)
    if not check_param_bool:
        return check_param_mess[0].text

    # Add headers to the request
    test_request.add_fromserver_request_authorization_token_header(session_user_id)

    # GET the URL
    base_url = TestReportService.create_base_url(Constants.TWO_ONE_ONE_CONSTANT, Constants.EMSP_CONSTANT,
                                                 Constants.TOKENS_CONSTANT, session_user_id)
    test_request.url = base_url + pg_param.build_uri_pagination()

    # Send request then build response
    try:
        response = test_request.send_get_request()
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
    result_bool_res_headers_pagination, result_tab_res_headers_pagination = response_headers.pagination_validation(offset=int(pg_param.offset) if pg_param.offset is not None else 0, limit=int(pg_param.limit) if pg_param.limit is not None else 9999999)
    result_tab.extend(result_tab_res_headers_pagination)
    if result_bool_http_status_code and result_bool_res_headers_ct_type and result_bool_res_headers_pagination:
        # Check du body
        response_body = BodyValidator(test_response.body)
        result_bool_json_body, result_tab_json_body = response_body.is_json_body()
        result_tab.extend(result_tab_json_body)
        if result_bool_json_body:
            test_response.body = json.loads(test_response.body)
            response_body = BodyValidator(test_response.body)
            result_bool_req_body, result_tab_req_body = response_body.schema_validator(self=response_body,
                                                                                       path_to_schema="app/api/utils/two_one_one/jsonschema/response/tokens/OCPI_V211_FromServer_get_emsp_tokens.json")
            result_tab.extend(result_tab_req_body)

    # Create test_report
    test_response.tests = result_tab
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_GET_emsp_Tokens,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.response),
                                                  web_service_id=iop_ws.webservice_id,
                                                  user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_cpo_211.route("/tokens<wildcard:path>", methods=['PATCH', 'PUT', 'DELETE', 'GET', 'POST'])
@requires_auth
def error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return Constants.ERROR_CONSTANT
