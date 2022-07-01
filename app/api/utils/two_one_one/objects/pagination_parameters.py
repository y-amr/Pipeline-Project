from app.api.utils.two_one_one.constants import Constants


class PaginationParameters:
    DATE_FROM_CONSTANT = 'date_from'
    DATE_TO_CONSTANT = 'date_to'
    LIMIT_CONSTANT = 'limit'
    OFFSET_CONSTANT = 'offset'

    def __init__(self, *args, **kwargs):
        # 1st constructor
        if kwargs.get('request') is not None:
            request = kwargs.get('request')
            if request.args.get(self.DATE_FROM_CONSTANT) is not None:
                self.date_from = request.args.get(self.DATE_FROM_CONSTANT)
            else:
                self.date_from = None
            if request.args.get(self.DATE_TO_CONSTANT) is not None:
                self.date_to = request.args.get(self.DATE_TO_CONSTANT)
            else:
                self.date_to = None
            if request.args.get(self.LIMIT_CONSTANT) is not None:
                self.limit = request.args.get(self.LIMIT_CONSTANT)
            else:
                self.limit = None
            if request.args.get(self.OFFSET_CONSTANT) is not None:
                self.offset = request.args.get(self.OFFSET_CONSTANT)
            else:
                self.offset = None
        # 2nd constructor
        elif kwargs.get('date_from') is not None:
            self.date_from = kwargs.get('date_from') if kwargs.get('date_from') != '' else None
            self.date_to = kwargs.get('date_to') if kwargs.get('date_to') is not None and kwargs.get(
                'date_to') != '' else None
            self.limit = kwargs.get('limit') if kwargs.get('limit') is not None and kwargs.get('limit') != '' else None
            self.offset = kwargs.get('offset') if kwargs.get('offset') is not None and kwargs.get(
                'offset') != '' else None

    def build_uri_pagination(self):
        first_param = True
        to_return = ''
        if self.date_from is not None:
            first_param = False
            to_return += Constants.QUESTION_TAG_CONSTANT + self.DATE_FROM_CONSTANT + Constants.EQUAL_CONSTANT + self.date_from
        if self.date_to is not None:
            if first_param:
                first_param = False
                to_return += Constants.QUESTION_TAG_CONSTANT + self.DATE_TO_CONSTANT + Constants.EQUAL_CONSTANT + self.date_to
            else:
                to_return += Constants.AND_CONSTANT + self.DATE_TO_CONSTANT + Constants.EQUAL_CONSTANT + self.date_to
        if self.limit is not None:
            if first_param:
                first_param = False
                to_return += Constants.QUESTION_TAG_CONSTANT + self.LIMIT_CONSTANT + Constants.EQUAL_CONSTANT + self.limit
            else:
                to_return += Constants.AND_CONSTANT + self.LIMIT_CONSTANT + Constants.EQUAL_CONSTANT + self.limit
        if self.offset is not None:
            if first_param:
                to_return += Constants.QUESTION_TAG_CONSTANT + self.OFFSET_CONSTANT + Constants.EQUAL_CONSTANT + self.offset
            else:
                to_return += Constants.AND_CONSTANT + self.OFFSET_CONSTANT + Constants.EQUAL_CONSTANT + self.offset
        return to_return
