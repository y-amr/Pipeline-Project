from sqlalchemy import Column, Integer, String,TIMESTAMP
from app.Base import Base


class IntegrationTestProcess(Base):
    __tablename__ = "integration_test_process"
    id = Column(Integer, primary_key=True)
    gireve_id = Column(String(64), primary_key=True)
    user_id = Column(String(128), nullable=False)
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)
    env_id = Column(String(128), nullable=False)
    uc_in_progress = Column(Integer)
    status = Column(String(128), nullable=False)


    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'gireve_id': self.gireve_id,
            'user_id': self.user_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'env_id': self.env_id,
            'uc_in_progress': self.uc_in_progress,
            'status': self.status,
        }

    @property
    def printable_form(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'gireve_id': self.gireve_id,
            'user_id': self.user_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'env_id': self.env_id,
            'uc_in_progress': self.uc_in_progress,
            'status': self.status,
        }
