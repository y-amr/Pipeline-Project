import logging

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app import db_session
from app.api.model.objects.integration_test import IntegrationTest
from app.api.model.objects.integration_test_process import IntegrationTestProcess
from app.api.model.objects.iop_use_case import IOPUseCase


class IntegrationTestService:

    @staticmethod
    def get_iop_usecases_by_name_type(name):
        return IOPUseCase.query.filter(IOPUseCase.name == name).one()

    # Return all test_report after the index
    @staticmethod
    def get_integration_test_process_from_index_by_env(index, env_id):
        return IntegrationTestProcess.query.filter(
            IntegrationTestProcess.id > index, IntegrationTestProcess.env_id == env_id).all()

        # Save test report (delete if more than MAX_REPORT in the database)

    @staticmethod
    def save_integration_test(integration_test):
        try:
            db_session.add(integration_test)
            db_session.commit()
        except SQLAlchemyError as e:
            logging.error(e.args)
            db_session.rollback()
        finally:
            db_session.remove()

    # Save processing_nr
    @staticmethod
    def save_integration_process_or_use_case(integration_process):
        try:
            db_session.merge(integration_process)
            db_session.commit()
        except SQLAlchemyError as e:
            logging.error(e.args)
            db_session.rollback()
        finally:
            db_session.remove()

    @staticmethod
    def convert_report_to_integration_test(test_report, test_use_case_id, num_request):
        return IntegrationTest(date_start=test_report.date_report, report=test_report.report,
                                   status=test_report.status,
                                   web_service_id=test_report.web_service_id, user_id=test_report.user_id,
                                   test_use_case_id=test_use_case_id, num_request=num_request)

    # Return the maxId
    @staticmethod
    def get_processing_nr_max_id_by_env_id(env_id):
        return db_session.query(func.max(IntegrationTestProcess.id).label('maxId')).filter(
            IntegrationTestProcess.env_id == env_id).one().maxId

    @staticmethod
    def find_non_regression_by_ws_id(ws_id, non_reg_id):
        try:
            Report_find = db_session.query(IntegrationTest).filter(
                IntegrationTest.web_service_id == ws_id, IntegrationTest.id == non_reg_id).order_by(IntegrationTest.id.desc()).first()
            if Report_find:
                return Report_find
            else:
                return False
        except SQLAlchemyError as e:
            logging.error(e.args)
            db_session.rollback()
        finally:
            db_session.remove()


