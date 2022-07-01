import json

import requests

from app.api.model.objects.parameter import Parameter
from app.api.model.services.parameter_service import ParameterService
from app.api.utils.two_one_one.constants import Constants


class Test:
    INFO = 'I'
    ERROR = 'E'
    WARNING = 'W'

    def __init__(self, level, text):
        self.level = level
        self.text = text

    def __str__(self):
        return json.dumps(self.serialize)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'level': self.level,
            'text': self.text
        }


class TestRequest:
    def __init__(self, url, headers, body, tests):
        self.url = url
        self.headers = headers
        self.body = body
        self.tests = tests

    @property
    def serialize(self):
        return {
            'url': self.url,
            'headers': [{k: v for k, v in self.headers.items()}] if self.headers is not None else {},
            'body': self.body if self.body is not None else {},
            'tests': [t.serialize for t in self.tests] if self.tests is not None else {}
        }

    def __str__(self):
        return json.dumps(self.serialize)

    # Check if parameters used to send request FromServer are defined for this user
    @staticmethod
    def check_fromserver_request_parameters(user_id):
        to_return_bool = True
        to_return_mess = ''
        # Check if Endpoint filled
        if not ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT, user_id):
            to_return_bool = False
            to_return_mess = 'please fill your endpoint in the parameters'
        # Check if token_from_iop filled
        elif not ParameterService.get_parameters_by_key_userid(Parameter.AUTHORISATION_TOKEN_FROMSERVER, user_id):
            to_return_bool = False
            to_return_mess = 'please fill the FromServer authorization token in the parameters'
        return to_return_bool, to_return_mess

    # Check if server country_code and party_id parameters are defined for this user
    @staticmethod
    def check_server_object_owner_parameters(user_id):
        to_return_bool = True
        to_return_mess = ''
        # Check if server country_code is filled
        if not ParameterService.get_parameters_by_key_userid(Parameter.SERVER_COUNTRY_CODE, user_id):
            to_return_bool = False
            to_return_mess = 'please fill server country_code in the parameters'
        # Check if server party_id is filled
        elif not ParameterService.get_parameters_by_key_userid(Parameter.SERVER_PARTY_ID, user_id):
            to_return_bool = False
            to_return_mess = 'please fill server party_id in the parameters'
        return to_return_bool, to_return_mess

    # Add authorization_token header to a FromServer request
    def add_fromserver_request_authorization_token_header(self, user_id):
        if self.headers is None:
            self.headers = {}
        self.headers[Constants.AUTHORIZATION_CONSTANT] = Constants.TOKEN_SPACE_CONSTANT + ParameterService.get_parameters_by_key_userid(Parameter.AUTHORISATION_TOKEN_FROMSERVER, user_id).value

    # Add content-type json header to a FromServer request
    def add_fromserver_request_content_type_json_header(self):
        if self.headers is None:
            self.headers = {}
        self.headers[Constants.CONTENT_TYPE_CONSTANT] = Constants.CONTENT_TYPE_APPLICATION_JSON_CONSTANT

    # Send this request as a POST request
    def send_post_request(self):
        return requests.post(self.url, data=json.dumps(self.body), headers=self.headers)

    # Send this request as a PUT request
    def send_put_request(self):
        return requests.put(self.url, data=json.dumps(self.body), headers=self.headers)

    # Send this request as a PATCH request
    def send_patch_request(self):
        return requests.patch(self.url, data=json.dumps(self.body), headers=self.headers)

    # Send this request as a GET request
    def send_get_request(self):
        return requests.get(self.url, headers=self.headers)

    # Send this request as a DELETE request
    def send_delete_request(self):
        return requests.delete(self.url, headers=self.headers)


class TestResponse:
    def __init__(self, headers, body, tests, http_status_code):
        self.headers = headers
        self.body = body
        self.tests = tests
        self.http_status_code = http_status_code

    @property
    def serialize(self):
        # to_return = {}
        # if self.headers is not None:
        #     to_return.update({'headers': [{k: v for k, v in self.headers}]})
        # if self.tests is not None:
        #     to_return.update({'tests': [t.serialize for t in self.tests]})
        # to_return.update({'body': self.body})
        # return to_return

        return {
            'headers': ([{k: v for k, v in self.headers.items()}] if self.headers is not None else {}),
            # 'data': ([i.serialize for i in self.data] if type(
            #     self.data) is list else self.data.serialize if self.data is not None else {}),
            'body': self.body,
            'tests': ([t.serialize for t in self.tests] if self.tests is not None else {}),
            'http_status_code': self.http_status_code
        }

    def __str__(self):
        return json.dumps(self.serialize)

    # Used to add the Link header
    @staticmethod
    def add_link_header(self, base_url, pagination_param, offset, limit):
        req = base_url
        is_first = True
        if pagination_param.date_from is not None:
            req += "?" + pagination_param.DATE_FROM_CONSTANT + "=" + pagination_param.date_from
            is_first = False
        if pagination_param.date_to is not None:
            if is_first:
                req += "?" + pagination_param.DATE_TO_CONSTANT + "=" + pagination_param.date_to
                is_first = False
            else:
                req += "&" + pagination_param.DATE_TO_CONSTANT + "=" + pagination_param.date_to
        if is_first:
            req += "?" + pagination_param.OFFSET_CONSTANT + "=" + str(offset + limit)
        else:
            req += "&" + pagination_param.OFFSET_CONSTANT + "=" + str(offset + limit)
        req += "&" + pagination_param.LIMIT_CONSTANT + "=" + str(limit)
        if self.headers is None:
            self.headers = {}
        self.headers[Constants.LINK_CONSTANT] = "<{}>;rel=\"next\"".format(req)

    # Used to add the Link header
    @staticmethod
    def add_pagination_headers(self, base_url, pagination_param, offset, req_limit, total_count, max_limit):
        # Security
        if self.headers is None:
            self.headers = {}
        # Add Limit and total-count headers
        self.headers[Constants.X_LIMIT_CONSTANT] = req_limit
        self.headers[Constants.X_TOTAL_COUNT_CONSTANT] = total_count
        # Add link header if needed
        if total_count > offset + req_limit:
            req = base_url
            is_first = True
            if pagination_param.date_from is not None:
                req += "?" + pagination_param.DATE_FROM_CONSTANT + "=" + pagination_param.date_from
                is_first = False
            if pagination_param.date_to is not None:
                if is_first:
                    req += "?" + pagination_param.DATE_TO_CONSTANT + "=" + pagination_param.date_to
                    is_first = False
                else:
                    req += "&" + pagination_param.DATE_TO_CONSTANT + "=" + pagination_param.date_to
            if is_first:
                req += "?" + pagination_param.OFFSET_CONSTANT + "=" + str(offset + req_limit)
            else:
                req += "&" + pagination_param.OFFSET_CONSTANT + "=" + str(offset + req_limit)
            req += "&" + pagination_param.LIMIT_CONSTANT + "=" + str(req_limit)
            self.headers[Constants.LINK_CONSTANT] = "<{}>;rel=\"next\"".format(req)


class Report:
    OK = 'OK'
    KO = 'KO'
    OK_BUT_WARNING = 'OK_BUT_WARNING'

    def __init__(self, test_request, test_response):
        self.request = test_request
        self.response = test_response

    @property
    def serialize(self):
        return {
            'request': self.request.serialize,
            'response': self.response.serialize
        }

    def __str__(self):
        return json.dumps(self.serialize)

    # Return the status of the report
    @staticmethod
    def get_status(to_test):
        to_return = Report.OK
        if to_test is not None and to_test.tests is not None:
            res = next((sub for sub in to_test.tests if sub.level == Test.ERROR), None)
            if res is not None:
                to_return = Report.KO
            else:
                res = next((sub for sub in to_test.tests if sub.level == Test.WARNING), None)
                if res is not None:
                    to_return = Report.OK_BUT_WARNING
        return to_return
