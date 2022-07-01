from app.api.model.objects.parameter import Parameter
from app.api.model.services.parameter_service import ParameterService
from app.api.utils.two_one_one.objects.test_report import Test
from app.api.utils.two_one_one.validators.timestamp_validator import TimeStampValidator


class URLValidator:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def object_owner_validation(country_code, party_id, user_id):
        # Init return table
        result_boolean = True
        results = []
        country_code_parameter = ParameterService.get_parameters_by_key_userid(Parameter.USER_COUNTRY_CODE, user_id)
        if country_code_parameter is None:
            results.append(Test(level=Test.ERROR, text="Please configure a 'Country Code' in parameters"))
            result_boolean = False
        elif country_code != country_code_parameter.value:
            results.append(Test(level=Test.ERROR,
                                text="The 'Country Code' sent doesn't match the parameter : " + country_code_parameter.value))
            result_boolean = False
        party_id_parameter = ParameterService.get_parameters_by_key_userid(Parameter.USER_PARTY_ID, user_id)
        if party_id_parameter is None:
            results.append(Test(level=Test.ERROR, text="Please configure a 'Party Id' in parameters"))
            result_boolean = False
        elif party_id != party_id_parameter.value:
            results.append(Test(level=Test.ERROR,
                                text="The 'Party Id' sent doesn't match the parameter : " + party_id_parameter.value))
            result_boolean = False
        if result_boolean:
            results.append(Test(level=Test.INFO,
                                text="URL Ok"))
        return result_boolean, results

    @staticmethod
    def is_positive_integer(integer_to_test):
        to_return = True
        try:
            val = int(integer_to_test)
            if val < 0:
                to_return = False
        except ValueError:
            to_return = False
        return to_return

    @staticmethod
    def pagination_validation(pagination_parameters):
        # Init return table
        result_boolean = True
        results = []
        if pagination_parameters.date_from is not None:
            if not TimeStampValidator.validate(pagination_parameters.date_from):
                results.append(Test(level=Test.ERROR,
                                    text="date_from parameter doesn't match the standard format"))
                result_boolean = False
        if pagination_parameters.date_to is not None:
            if not TimeStampValidator.validate(pagination_parameters.date_from):
                results.append(Test(level=Test.ERROR,
                                    text="date_to parameter doesn't match the standard format"))
                result_boolean = False
        if pagination_parameters.offset is not None:
            if not URLValidator.is_positive_integer(pagination_parameters.offset):
                results.append(Test(level=Test.ERROR,
                                    text="offset is not a positive integer"))
                result_boolean = False
        if pagination_parameters.limit is not None:
            if not URLValidator.is_positive_integer(pagination_parameters.limit):
                results.append(Test(level=Test.ERROR,
                                    text="limit is not a positive integer"))
                result_boolean = False
        if result_boolean:
            results.append(Test(level=Test.INFO,
                                text="pagination parameters Ok"))
        return result_boolean, results

    def __str__(self):
        return self.url
