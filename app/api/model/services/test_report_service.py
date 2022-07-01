import logging

from sqlalchemy import func, null, update
from sqlalchemy.exc import SQLAlchemyError
from app import db_session
from app.api.model.objects.parameter import Parameter
from app.api.model.objects.test_report import TestReport
from decouple import config
from app.api.model.services.parameter_service import ParameterService
from app.api.utils.two_one_one.constants import Constants


class TestReportService:

    # Return all test_report after the index
    @staticmethod
    def get_test_report_from_index_by_userid(index, user_id):
        return TestReport.query.filter(
            TestReport.id > index, TestReport.user_id == user_id).all()

    # Save test report (delete if more than MAX_REPORT in the database)
    @staticmethod
    def save_test_report(test_report):
        try:
            if db_session.query(TestReport.id).filter(TestReport.user_id == test_report.user_id).count() > int(
                    config('MAX_TEST_REPORT_DISPLAY')):
                maxId = db_session.query(func.max(TestReport.id).label('maxId')).filter(
                    TestReport.user_id == test_report.user_id).one().maxId
                reportToDelete = db_session.query(TestReport).filter(
                    TestReport.id <= (maxId - int(config('MAX_TEST_REPORT_DISPLAY')) + 1),
                    TestReport.user_id == test_report.user_id).all()
                for report in reportToDelete:
                    db_session.delete(report)
            db_session.add(test_report)
            db_session.commit()
        except SQLAlchemyError as e:
            logging.error(e.args)
            db_session.rollback()
        finally:
            db_session.remove()

    # Return the maxId
    @staticmethod
    def get_test_report_max_id_by_userid(user_id):
        return db_session.query(func.max(TestReport.id).label('maxId')).filter(
            TestReport.user_id == user_id).one().maxId


    @staticmethod
    def find_test_report_by_ws_id(user_id, ws_id, date):
        return TestReport.query.filter(
            TestReport.web_service_id == ws_id, TestReport.user_id == user_id, TestReport.date_report <= date). \
            order_by(TestReport.id.desc()).first()

    @staticmethod
    def create_base_url(version, role, module, session_user_id):
        # GET the URL
        parameter = Constants.ENDPOINT_CONSTANT + Constants.UNDERSCORE_CONSTANT + version + Constants.UNDERSCORE_CONSTANT + role + Constants.UNDERSCORE_CONSTANT + module
        if ParameterService.get_parameters_by_key_userid(parameter, session_user_id):
            return ParameterService.get_parameters_by_key_userid(parameter, session_user_id).value
        else:
            # If no specific endpoint was specified : BUILD the URL from ENDPOINT
            constant_parameters = Constants.TO_CONSTANT + Constants.UNDERSCORE_CONSTANT + role + Constants.UNDERSCORE_CONSTANT + module + Constants.UNDERSCORE_CONSTANT + version + Constants.UNDERSCORE_CONSTANT + Constants.ENDPOINT_CONSTANT + Constants.UNDERSCORE_CONSTANT + Constants.CONSTANT_CONSTANT
            user_endpoint = ParameterService.get_parameters_by_key_userid(Parameter.ENDPOINT, session_user_id).value
            return user_endpoint + getattr(Constants, constant_parameters)
