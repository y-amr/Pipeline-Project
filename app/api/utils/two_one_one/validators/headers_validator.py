import re

from app.api.model.objects.parameter import Parameter
from app.api.model.services.parameter_service import ParameterService
from app.api.utils.two_one_one.constants import Constants
from app.api.utils.two_one_one.helper import Helper
from app.api.utils.two_one_one.objects.test_report import Test


class HeadersValidator:

    def __init__(self, request_headers):
        self.request_headers = request_headers

    # Validation standard HeadersValidator
    def standard_validation(self, user_id):
        # Init return table
        result_boolean = True
        results = []
        if self.request_headers.get(Constants.AUTHORIZATION_CONSTANT) is None:
            results.append(Test(level=Test.ERROR, text="No 'Authorization' header"))
            result_boolean = False
        else:
            authorization_key = ParameterService.get_parameters_by_key_userid(Parameter.AUTHORISATION_TOKEN_TOSERVER,
                                                                              user_id)
            if authorization_key is None:
                results.append(
                    Test(level=Test.ERROR, text="Please configure an Authorization token ToServer in parameters"))
                result_boolean = False
            elif self.request_headers.get(
                    Constants.AUTHORIZATION_CONSTANT) != Constants.TOKEN_SPACE_CONSTANT + authorization_key.value:
                results.append(Test(level=Test.ERROR,
                                    text="The Authorization Token sent doesn't respect the pattern, it should be : '" + Constants.TOKEN_SPACE_CONSTANT + authorization_key.value + "'"))
                result_boolean = False
        return result_boolean, results

    # In case of GET ToServer, the request shouldn't contain content-type header
    def no_content_type_validation(self):
        # Init return table
        result_boolean = True
        results = []
        if self.request_headers.get(Constants.CONTENT_TYPE_CONSTANT) is not None or self.request_headers.get(
                Constants.CONTENT_TYPE_CONSTANT.lower()) is not None:
            results.append(Test(level=Test.ERROR, text="GET requests should not contain a content-type header"))
            result_boolean = False
        return result_boolean, results

    # In case of  FromServer with data, the request should contain content-type:application/json header
    def content_type_json_validation(self):
        # Init return table
        result_boolean = True
        results = []
        if not self.request_headers.get(Constants.CONTENT_TYPE_CONSTANT) is None:
            if not Constants.CONTENT_TYPE_APPLICATION_JSON_CONSTANT.lower() in self.request_headers.get(
                    Constants.CONTENT_TYPE_CONSTANT).lower():
                results.append(
                    Test(level=Test.ERROR,
                         text="Headers should contain a " + Constants.CONTENT_TYPE_CONSTANT + ":" + Constants.CONTENT_TYPE_APPLICATION_JSON_CONSTANT + " header"))
                result_boolean = False
        elif not self.request_headers.get(Constants.CONTENT_TYPE_CONSTANT.lower()) is None:
            if not Constants.CONTENT_TYPE_APPLICATION_JSON_CONSTANT.lower() in self.request_headers.get(
                    Constants.CONTENT_TYPE_CONSTANT.lower()).lower():
                results.append(
                    Test(level=Test.ERROR,
                         text="Headers should contain a " + Constants.CONTENT_TYPE_CONSTANT + ":" + Constants.CONTENT_TYPE_APPLICATION_JSON_CONSTANT + " header"))
                result_boolean = False
        else:
            results.append(
                Test(level=Test.ERROR,
                     text="Headers should contain a " + Constants.CONTENT_TYPE_CONSTANT + ":" + Constants.CONTENT_TYPE_APPLICATION_JSON_CONSTANT + " header"))
            result_boolean = False
        return result_boolean, results

    # In case of  GET webservices using pagination, the pagination headers must be present
    def pagination_validation(self, offset, limit):
        # Init return table
        result_boolean = True
        results = []
        if self.request_headers.get(Constants.X_TOTAL_COUNT_CONSTANT) is None:
            results.append(
                Test(level=Test.ERROR,
                     text="Headers should contain a " + Constants.X_TOTAL_COUNT_CONSTANT + " header"))
            result_boolean = False
        else:
            try:
                int(self.request_headers.get(Constants.X_TOTAL_COUNT_CONSTANT))
            except Exception:
                results.append(Test(level=Test.ERROR,
                                    text=Constants.X_TOTAL_COUNT_CONSTANT + " header should be an integer"))
                result_boolean = False
        if self.request_headers.get(Constants.X_LIMIT_CONSTANT) is None:
            results.append(
                Test(level=Test.ERROR,
                     text="Headers should contain a " + Constants.X_LIMIT_CONSTANT + " header"))
            result_boolean = False
        else:
            try:
                int(self.request_headers.get(Constants.X_LIMIT_CONSTANT))
            except Exception:
                results.append(Test(level=Test.ERROR,
                                    text=Constants.X_LIMIT_CONSTANT + " header should be an integer"))
                result_boolean = False
        # If no error, check if Link header should be present
        if result_boolean:
            min_limit = min(limit, int(self.request_headers.get(Constants.X_LIMIT_CONSTANT)))
            if min_limit + offset < int(self.request_headers.get(Constants.X_TOTAL_COUNT_CONSTANT)):
                if self.request_headers.get(Constants.LINK_CONSTANT) is None:
                    results.append(
                        Test(level=Test.ERROR,
                             text="Headers should contain a " + Constants.LINK_CONSTANT + " header"))
                    result_boolean = False
                else:
                    result = re.search(Constants.SEARCH_PAGINATION_CONSTANT,
                                       self.request_headers.get(Constants.LINK_CONSTANT).replace(" ", ""))
                    good_url_bool = False
                    if result is not None and result.group(1) is not None:
                        if Helper.is_valid_url(result.group(1)):
                            good_url_bool = True
                    if not good_url_bool:
                        results.append(
                            Test(level=Test.ERROR,
                                 text="Headers should contain a " + Constants.LINK_CONSTANT + ' header with pattern : <{URL_OF_THE_NEXT_PAGE}>;rel="next"'))
                        result_boolean = False
        return result_boolean, results

    # In case of  POST_emsp_Cdrs, the header response should contain a 'Location' URL
    def location_url_format_validation(self):
        # Init return table
        result_boolean = True
        results = []
        if self.request_headers.get(Constants.LOCATION_CONSTANT) is None or not Helper.is_valid_url(
                self.request_headers.get(Constants.LOCATION_CONSTANT)):
            results.append(
                Test(level=Test.ERROR,
                     text="Headers should contain a " + Constants.LOCATION_CONSTANT + " header with a valid url format"))
            result_boolean = False
        return result_boolean, results
