from app.api.utils.two_one_one.helper import Helper


class OCPIResponse:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def response_success(self, message):
        response = {
            "data": ([i.serialize for i in self.data] if isinstance(self.data,
                                                                    list) else self.data if self.data is not None else {}),
            "status_code": 1000,
            "status_message": (message if message is not None and message != "" else "Success"),
            "timestamp": Helper.get_current_timestamp()}
        return response

    @staticmethod
    def response_error(message, error_code):
        response = {
            "data": {},
            "status_code": error_code,
            "status_message": message,
            "timestamp": Helper.get_current_timestamp()}
        return response
