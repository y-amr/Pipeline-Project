from sqlalchemy import Column, Integer, String, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import relationship

from app.Base import Base
from app.api.model.objects.iop_webservice import IOPWebservice


class IntegrationTest(Base):
    __tablename__ = "integration_test"
    id = Column(Integer, primary_key=True)
    test_use_case_id = Column(Integer)
    date_start = Column(TIMESTAMP)
    num_request = Column(Integer)
    report = Column(JSON)
    status = Column(String(64))
    web_service_id = Column(Integer, ForeignKey(IOPWebservice.webservice_id))
    use_cases_id = Column(Integer)
    user_id = Column(String(128), nullable=False)
    iop_webservice = relationship(IOPWebservice)


    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'test_use_case_id': self.test_use_case_id,
            'date_start': self.date_start,
            'num_request': self.num_request,
            'report': self.report,
            'status': self.status,
            'web_service_id': self.web_service_id,
            'use_cases_id': self.use_cases_id,
            'user_id': self.user_id
        }

    @property
    def printable_form(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'test_use_case_id': self.test_use_case_id,
            'use_cases_id': self.use_cases_id,
            'num_request': self.num_request,
            'date_start': self.date_start.isoformat(),
            'report': self.report,
            'status': self.status,
            'web_service_id': self.web_service_id,
            'iop_webservice_name': (self.iop_webservice.webservice_name if self.iop_webservice is not None else ''),
            'ocpi_module_name': (self.iop_webservice.ocpi_module.module_name if self.iop_webservice is not None else ''),
            'ocpi_role_name': (self.iop_webservice.ocpi_role.role_name if self.iop_webservice is not None else ''),
            'iop_webservice_type': (self.iop_webservice.type if self.iop_webservice is not None else ''),
            'user_id': self.user_id
        }
