from sqlalchemy import Column, Integer, String
from app.Base import Base


class IOPUseCase(Base):
    UC_NAME_POST_tokens_authorize = "post_token_authorize"
    UC_NAME_PUT_cpo_Tokens = "PUT_cpo_Tokens"

    __tablename__ = "iop_use_case"
    id = Column(Integer, primary_key=True)
    major_id = Column(Integer)
    minor_id = Column(Integer)
    name = Column(String(64))
    description = Column(String(256))


    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'major_id': self.major_id,
            'minor_id': self.minor_id,
            'name': self.name,
            'description': self.description
        }

    @property
    def printable_form(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'major_id': self.major_id,
            'minor_id': self.minor_id,
            'name': self.name,
            'description': self.description
        }
