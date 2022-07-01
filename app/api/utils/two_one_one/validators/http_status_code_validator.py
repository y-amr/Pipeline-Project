from flask_api import status

from app.api.utils.two_one_one.objects.test_report import Test


class HttpStatusCodeValidator:
    @staticmethod
    def http_status_success_validation(http_status):
        result_boolean = True
        results = []
        if not status.is_success(http_status):
            result_boolean = False
            results.append(Test(level=Test.ERROR, text="HTTP status code is not Success (2xx)"))
        return result_boolean, results
