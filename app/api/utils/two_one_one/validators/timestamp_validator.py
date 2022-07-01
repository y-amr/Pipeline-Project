import datetime


class TimeStampValidator:
    @staticmethod
    def validate(timestamp_date):
        toReturn = True
        if timestamp_date is not None and timestamp_date != '':
            try:
                datetime.datetime.strptime(timestamp_date, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                try:
                    datetime.datetime.strptime(timestamp_date, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    toReturn = False
        else:
            toReturn = False
        return toReturn
