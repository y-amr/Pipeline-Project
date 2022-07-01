import json
import logging

from flask import session, request
from flask_api import status
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
from app.api.utils.two_one_one.objects.test_report import TestRequest, TestResponse, Report, Test
from app.api.utils.two_one_one.validators.body_validator import BodyValidator
from app.api.utils.two_one_one.validators.headers_validator import HeadersValidator
from app.api.utils.two_one_one.validators.http_status_code_validator import HttpStatusCodeValidator
from app.authentication import requires_auth


@fromserver_cpo_211.route("/tariffs/PUT_emsp_Tariffs", methods=['POST'])
@requires_auth
def fromserver_put_emsp_tariffs():
    session_user_id = session['profile'].get('user_id')
    # creation de la requete a envoyer
    # Init result table
    result_tab = []
    test_request = TestRequest(url=None, headers=None, body=None, tests=None)

    # Check if user parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_fromserver_request_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Check if server parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_server_object_owner_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Add headers to the request
    test_request.add_fromserver_request_content_type_json_header()
    test_request.add_fromserver_request_authorization_token_header(session_user_id)
    # création du body a envoyer d'aprés les données rentrée par l'utilisateur
    try:
        test_request.body = json.loads(request.get_json().get("request_template"))
    except ValueError:
        return "Please fill a json request"

    # Check session_id consistency
    body_session_id = test_request.body.get("id")
    form_tariff_id = request.get_json().get("tariff_id")
    if form_tariff_id is None or form_tariff_id == '':
        form_tariff_id = Constants.DEFAULT_ID_CONSTANT
    if body_session_id is None or body_session_id != form_tariff_id:
        return "The 'tariff.id' in the body doesn't match the one in the URL"

    server_country_code = ParameterService.get_parameters_by_key_userid(Parameter.SERVER_COUNTRY_CODE,
                                                                        session_user_id).value
    server_party_id = ParameterService.get_parameters_by_key_userid(Parameter.SERVER_PARTY_ID, session_user_id).value

    # CREATE URL
    base_url = TestReportService.create_base_url(Constants.TWO_ONE_ONE_CONSTANT, Constants.EMSP_CONSTANT,
                                                 Constants.TARIFFS_CONSTANT, session_user_id)
    test_request.url = base_url + Constants.SLASH_CONSTANT + server_country_code + Constants.SLASH_CONSTANT + server_party_id + Constants.SLASH_CONSTANT + form_tariff_id

    # Send request then build response
    try:
        response = test_request.send_put_request()
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
                                                                                       path_to_schema="app/api/utils/two_one_one/jsonschema/response/OCPI_V211_FromServer_standard_response_no_data.json")
            result_tab.extend(result_tab_req_body)

    # Create test_report
    test_response.tests = result_tab
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_PUT_emsp_Tariffs,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.response),
                                                  web_service_id=iop_ws.webservice_id,
                                                  user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_cpo_211.route("/tariffs/PATCH_emsp_Tariffs", methods=['POST'])
@requires_auth
def fromserver_patch_emsp_tariffs():
    session_user_id = session['profile'].get('user_id')
    # creation de la requete a envoyer
    # Init result table
    result_tab = []
    test_request = TestRequest(url=None, headers=None, body=None, tests=None)

    # Check if user parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_fromserver_request_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Check if server parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_server_object_owner_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Add headers to the request
    test_request.add_fromserver_request_content_type_json_header()
    test_request.add_fromserver_request_authorization_token_header(session_user_id)
    # création du body a envoyer d'aprés les données rentrée par l'utilisateur
    try:
        test_request.body = json.loads(request.get_json().get("request_template"))
    except ValueError:
        return "Please fill a json request"

    # Check session_id consistency
    body_session_id = test_request.body.get("id")
    form_tariff_id = request.get_json().get("tariff_id")
    if form_tariff_id is None or form_tariff_id == '':
        form_tariff_id = Constants.DEFAULT_ID_CONSTANT
    if body_session_id is not None and body_session_id != form_tariff_id:
        return "The 'tariff.id' in the body doesn't match the one in the URL"

    server_country_code = ParameterService.get_parameters_by_key_userid(Parameter.SERVER_COUNTRY_CODE,
                                                                        session_user_id).value
    server_party_id = ParameterService.get_parameters_by_key_userid(Parameter.SERVER_PARTY_ID, session_user_id).value
    # CREATE URL
    base_url = TestReportService.create_base_url(Constants.TWO_ONE_ONE_CONSTANT, Constants.EMSP_CONSTANT,
                                                 Constants.TARIFFS_CONSTANT, session_user_id)
    test_request.url = base_url + Constants.SLASH_CONSTANT + server_country_code + Constants.SLASH_CONSTANT + server_party_id + Constants.SLASH_CONSTANT + form_tariff_id

    # Send request then build response
    try:
        response = test_request.send_patch_request()
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
                                                                                       path_to_schema="app/api/utils/two_one_one/jsonschema/response/OCPI_V211_FromServer_standard_response_no_data.json")
            result_tab.extend(result_tab_req_body)

    # Create test_report
    test_response.tests = result_tab
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_PATCH_emsp_Tariffs,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.response),
                                                  web_service_id=iop_ws.webservice_id,
                                                  user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_cpo_211.route("/tariffs/GET_emsp_Tariffs", methods=['POST'])
@requires_auth
def fromserver_get_emsp_tariffs():
    session_user_id = session['profile'].get('user_id')
    # creation de la requete a envoyer
    # Init result table
    result_tab = []
    test_request = TestRequest(url=None, headers=None, body=None, tests=None)

    # Check if user parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_fromserver_request_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Check if server parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_server_object_owner_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Add headers to the request
    test_request.add_fromserver_request_authorization_token_header(session_user_id)

    # Build the URL
    form_tariff_id = request.get_json().get("tariff_id")
    if form_tariff_id is None or form_tariff_id == '':
        form_tariff_id = Constants.DEFAULT_ID_CONSTANT
    server_country_code = ParameterService.get_parameters_by_key_userid(Parameter.SERVER_COUNTRY_CODE,
                                                                        session_user_id).value
    server_party_id = ParameterService.get_parameters_by_key_userid(Parameter.SERVER_PARTY_ID, session_user_id).value

    # CREATE URL
    base_url = TestReportService.create_base_url(Constants.TWO_ONE_ONE_CONSTANT, Constants.EMSP_CONSTANT,
                                                 Constants.TARIFFS_CONSTANT, session_user_id)
    test_request.url = base_url + Constants.SLASH_CONSTANT + server_country_code + Constants.SLASH_CONSTANT + server_party_id + Constants.SLASH_CONSTANT + form_tariff_id

    # Send request then build response
    try:
        response = test_request.send_get_request()
    except Exception as e:
        logging.error("Error during request for user : " + session_user_id + " => " + e.args.__str__())
        return "Error during request =>" + e.args.__str__()

    test_response = TestResponse(headers=response.headers, tests=None, body=response.text,
                                 http_status_code=response.status_code)

    # If not found, response OK
    if not test_response.http_status_code == status.HTTP_404_NOT_FOUND:
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
                                                                                           path_to_schema="app/api/utils/two_one_one/jsonschema/response/tariffs/OCPI_V211_FromServer_get_emsp_tariffs.json")
                result_tab.extend(result_tab_req_body)
                if result_bool_req_body:
                    if form_tariff_id != test_response.body.get('data').get('id'):
                        result_tab.append(
                            Test(level=Test.ERROR, text="The 'tariff.id' returned doesn't match the Tariff requested"))

    # Create test_report
    test_response.tests = result_tab
    test_report = Report(test_request, test_response)
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_ocpiversion_name_type(ocpiversion=OCPIVersion.two_one_one,
                                                                              name=IOPWebservice.WS_NAME_GET_emsp_Tariffs,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.response),
                                                  web_service_id=iop_ws.webservice_id,
                                                  user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_cpo_211.route("/tariffs/DELETE_emsp_Tariffs", methods=['POST'])
@requires_auth
def fromserver_delete_emsp_tariffs():
    session_user_id = session['profile'].get('user_id')
    # creation de la requete a envoyer
    # Init result table
    result_tab = []
    test_request = TestRequest(url=None, headers=None, body=None, tests=None)

    # Check if user parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_fromserver_request_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Check if server parameters are defined
    valid_param_bool, valid_param_mess = test_request.check_server_object_owner_parameters(session_user_id)
    if not valid_param_bool:
        return valid_param_mess

    # Add headers to the request
    test_request.add_fromserver_request_authorization_token_header(session_user_id)

    # Build the URL
    form_tariff_id = request.get_json().get("tariff_id")
    if form_tariff_id is None or form_tariff_id == '':
        form_tariff_id = Constants.DEFAULT_ID_CONSTANT
    server_country_code = ParameterService.get_parameters_by_key_userid(Parameter.SERVER_COUNTRY_CODE,
                                                                        session_user_id).value
    server_party_id = ParameterService.get_parameters_by_key_userid(Parameter.SERVER_PARTY_ID, session_user_id).value
    # CREATE URL
    base_url = TestReportService.create_base_url(Constants.TWO_ONE_ONE_CONSTANT, Constants.EMSP_CONSTANT,
                                                 Constants.TARIFFS_CONSTANT, session_user_id)
    test_request.url = base_url + Constants.SLASH_CONSTANT + server_country_code + Constants.SLASH_CONSTANT + server_party_id + Constants.SLASH_CONSTANT + form_tariff_id

    # Send request then build response
    try:
        response = test_request.send_delete_request()
    except Exception as e:
        logging.error("Error during request for user : " + session_user_id + " => " + e.args.__str__())
        return "Error during request =>" + e.args.__str__()

    test_response = TestResponse(headers=response.headers, tests=None, body=response.text,
                                 http_status_code=response.status_code)

    # If not found, response OK
    if not test_response.http_status_code == status.HTTP_404_NOT_FOUND:
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
                                                                              name=IOPWebservice.WS_NAME_DELETE_emsp_Tariffs,
                                                                              ws_type=IOPWebservice.TYPE_FROMSERVER
                                                                              )
    # Enregistrement du rapport de test
    TestReportService.save_test_report(TestReport(date_report=func.now(), report=test_report.serialize,
                                                  status=test_report.get_status(test_report.response),
                                                  web_service_id=iop_ws.webservice_id,
                                                  user_id=session_user_id))
    return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT


@fromserver_cpo_211.route("/tariffs<wildcard:path>", methods=['PATCH', 'PUT', 'DELETE', 'GET', 'POST'])
@requires_auth
def fromserver_cpo_tariffs_error_no_ws(path):
    logging.error("Webservice not standard : " + request.url)
    return Constants.ERROR_CONSTANT
