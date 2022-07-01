from sqlalchemy import Column, Integer, String, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import relationship

from app.Base import Base
from app.api.model.objects.iop_webservice import IOPWebservice


class TestReport(Base):
    __tablename__ = "test_report"
    id = Column(Integer, primary_key=True)
    date_report = Column(TIMESTAMP)
    report = Column(JSON)
    status = Column(String(64))
    web_service_id = Column(Integer, ForeignKey(IOPWebservice.webservice_id))
    iop_webservice = relationship(IOPWebservice)
    user_id = Column(String(128), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'date_report': self.date_report,
            'id': self.id,
            'report': self.report,
            'status': self.status,
            'web_service_id': self.web_service_id,
            'user_id': self.user_id
        }

    @property
    def printable_form(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'date_report': self.date_report.isoformat(),
            'report': self.report,
            'status': self.status,
            'web_service_id': self.web_service_id,
            'iop_webservice_name': (self.iop_webservice.webservice_name if self.iop_webservice is not None else ''),
            'ocpi_module_name': (self.iop_webservice.ocpi_module.module_name if self.iop_webservice is not None else ''),
            'ocpi_role_name': (self.iop_webservice.ocpi_role.role_name if self.iop_webservice is not None else ''),
            'iop_webservice_type': (self.iop_webservice.type if self.iop_webservice is not None else ''),
            'user_id': self.user_id
        }
