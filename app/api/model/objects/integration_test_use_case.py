from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from app.Base import Base
from app.api.model.objects.integration_test_process import IntegrationTestProcess
from app.api.model.objects.iop_use_case import IOPUseCase


class IntegrationTestUseCase(Base):
    __tablename__ = "integration_test_use_case"
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey(IntegrationTestProcess.id))
    use_case_id = Column(Integer, ForeignKey(IOPUseCase.id))
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)
    report = Column(String(128), nullable=False)
    status = Column(String(128), nullable=False)
    integration_test_process = relationship(IntegrationTestProcess)
    iop_use_case = relationship(IOPUseCase)



    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'process_id': self.process_id,
            'use_case_id': self.use_case_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'report': self.report,
            'status': self.status,
        }

    @property
    def printable_form(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'process_id': self.process_id,
            'use_case_id': self.use_case_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'report': self.report,
            'status': self.status,
        }
