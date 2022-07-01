import random
import re
import uuid
from urllib.parse import urlsplit, parse_qs

from flask import render_template, request, session
from sqlalchemy import func

from app.api.client.two_one_one.cpo.fromserver_cpo_tokens import fromserver_post_emsp_tokens_authorize
from app.api.client.two_one_one.emsp.fromserver_emsp_locations import fromserver_get_cpo_locations
from app.api.model.objects.integration_test_process import IntegrationTestProcess
from app.api.model.objects.integration_test_use_case import IntegrationTestUseCase
from app.api.model.objects.iop_use_case import IOPUseCase
from app.api.model.services.integration_test_service import IntegrationTestService
from app.api.model.services.test_report_service import TestReportService
from app.api.utils.two_one_one.constants import Constants
from app.api.web.non_reg import web_non_reg_api
from app import app
from app.authentication import requires_auth


@web_non_reg_api.route("", methods=['GET'])
@requires_auth
def iop_test_render():
    return render_template("non_reg/index.html", title='Parameters', version=app.config['VERSION'])

@web_non_reg_api.route("", methods=['POST'])
def iop_test():
    if request.method == 'POST':
        data_request = request.get_json()
        gireve_id = uuid.uuid4().__str__()
        user_id = session['profile'].get('user_id')
        env_id = data_request.get("env")
        start_date = func.now()
        num_request = 0
        IntegrationTestService.save_integration_process_or_use_case(IntegrationTestProcess(gireve_id=gireve_id, user_id=user_id,
                                                          env_id=env_id, start_date=start_date, status="PENDING"))
        IntegrationTestService.save_integration_process_or_use_case(IntegrationTestUseCase(use_case_id=IntegrationTestService.get_iop_usecases_by_name_type(
                                                  IOPUseCase.UC_NAME_POST_tokens_authorize),process_id=1,start_date=start_date,status=Constants.RUNNING_CONSTANT))

        # TOKEN AUTHORIZE
        request_data = {"token_uid": "12345ABCDEF",
                        "location_id": 'FRS1814102',
                        "evse_id": 'FR*YAM*E1231322'}
        fromserver_post_emsp_tokens_authorize(True, env_id, gireve_id,
                                               num_request, request_data)
        num_request = num_request + 1

        # Il me faut un TestReport avec le ID de web_service a 5 ( ToServer_POST_emsp_Tokens-authorize)
        IntegrationTestService.save_integration_process_or_use_case(IntegrationTestProcess(gireve_id=gireve_id, user_id=user_id,
                                                          env_id=env_id, status="ACTIVE"))
        IntegrationTestService.save_integration_process_or_use_case(IntegrationTestUseCase(use_case_id=IntegrationTestService.get_iop_usecases_by_name_type(
                                                  IOPUseCase.UC_NAME_POST_tokens_authorize),process_id=1,start_date=start_date,status=Constants.RUNNING_CONSTANT))

        post_tokens_request = TestReportService.find_test_report_by_ws_id(user_id, 5, start_date)
        if post_tokens_request:
            IntegrationTestService.save_integration_test(IntegrationTestService.convert_report_to_integration_test(post_tokens_request, use_case_post_token_authorize, non_regression_id, 2))

        #nouvelle table integration test use case : Id technique integration process, Id use case, status, result (string)
        IntegrationTestService.save_integration_process_or_use_case(ProcessingNr(non_regression_id=non_regression_id,
                                                          uc_in_progress=use_case_post_token_authorize))
        request_data = {
            "date_from": "",
            "date_to": "",
            'limit': "100",
            'offset': "0"
        }
        i = 1
        fromserver_get_cpo_locations(True, env_id, non_regression_id, 2, i, data)
        get_location = IntegrationTestService.find_non_regression_by_ws_id(62, non_regression_id, start_date)
        if get_location:
            while "Link" in get_location.report.get('response').get("headers")[0]:
                result = re.search(Constants.SEARCH_PAGINATION_CONSTANT,
                                   get_location.report.
                                   get('response').
                                   get("headers")[0].
                                   get(Constants.LINK_CONSTANT).replace(" ", ""))
                url = urlsplit(result.group(1)).query
                params = parse_qs(url)
                var = {k: v[0] for k, v in params.items()}
                data["limit"] = var.get("limit")
                data["offset"] = var.get("offset")
                i = i + 1
                fromserver_get_cpo_locations(True, env_id, non_regression_id, 2, i, data)
                get_location = TestReportService.find_non_regression_by_ws_id(62, non_regression_id, start_date)
        TestReportService.save_processing_nr(ProcessingNr(non_regression_id=non_regression_id, uc_in_progress=2))

        TestReportService.save_processing_nr(ProcessingNr(non_regression_id=non_regression_id, status="COMPLETED"))

        return Constants.REQUEST_SENT_SUCCESSFULLY_MESSAGE_CONSTANT
