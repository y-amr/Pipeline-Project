import logging

from sqlalchemy.exc import SQLAlchemyError

from app import db_session
from app.api.model.objects.parameter import Parameter
from app.api.utils.two_one_one.constants import Constants


class ParameterService:

    # Return all parameters from the 'Parameter' table
    @staticmethod
    def get_all_parameters_by_userid(user_id):
        return Parameter.query.filter_by(user_id=user_id).all()

    # Save parameters
    @staticmethod
    def save_parameters(parameters):
        try:
            for par in parameters:
                db_session.merge(par)
            db_session.commit()
        except SQLAlchemyError as e:
            logging.error(e.args)
            db_session.rollback()
        finally:
            db_session.remove()

    # Get a parameter by its key
    @staticmethod
    def get_parameters_by_key_userid(key_value, user_id):
        param = None
        try:
            param = Parameter.query.filter_by(key=key_value, user_id=user_id).one()
        except SQLAlchemyError as e:
            return False
        finally:
            return param
