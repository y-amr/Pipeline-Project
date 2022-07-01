import json
from datetime import datetime, timedelta
import time
import random
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class Helper:
    @staticmethod
    def get_current_timestamp():
        return "{}{}".format(datetime.utcnow().isoformat(sep='T', timespec='seconds'), "Z")

    @staticmethod
    def get_random_timestamp_with_range(date_from, date_to):
        time_format = "%Y-%m-%dT%H:%M:%S%z"
        s_time = time.mktime(time.strptime(date_from, time_format))
        e_time = time.mktime(time.strptime(date_to, time_format))
        p_time = s_time + random.random() * (e_time - s_time)
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(p_time)) + 'Z'

    @staticmethod
    def is_json(my_json):
        try:
            json_object = json.loads(my_json)
        except ValueError as e:
            return False
        return True

    @staticmethod
    def return_standard_ocpi_211_display_text():
        return {"language": "EN", "text": "OCPI tester created by GIREVE"}

    @staticmethod
    def is_valid_url(url):
        validate = URLValidator()
        try:
            validate(url)
            return True
        except ValidationError:
            return False
