import decimal
import json

import jsonschema
from jsonschema import validate

from app.api.utils.two_one_one.helper import Helper
from app.api.utils.two_one_one.objects.test_report import Test


class BodyValidator:
    def __init__(self, body):
        self.body = body

    @staticmethod
    def schema_validator(self, path_to_schema):
        result = []
        try:
            with open(path_to_schema, "r") as fichier:
                dict_valid = json.load(fichier, parse_float=decimal.Decimal)
            # Bad Trick to validate decimals :(
            validate(json.loads(json.dumps(self.body), parse_float=decimal.Decimal), dict_valid)
        except jsonschema.exceptions.ValidationError as valid_err:
            result.append(Test(level=Test.ERROR,
                               text=valid_err.message))
            return False, result
        result.append(Test(level=Test.INFO,
                           text="Body Ok"))
        return True, result

    # Check if the body is a json
    def is_json_body(self):
        result = []
        bool_return = True
        if not Helper.is_json(self.body):
            bool_return = False
            result.append(Test(level=Test.ERROR,
                               text="The body content is not json formatted"))
        return bool_return, result
