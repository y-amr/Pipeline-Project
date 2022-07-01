from sqlalchemy import Column, Integer, ForeignKey, String, event

from app.Base import Base, db_session
from app.api.model.objects.ocpi_version import OCPIVersion


class OCPIModule(Base):
    __tablename__ = 'ocpi_module'
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey(OCPIVersion.id))
    module_name = Column(String(128))

    def __repr__(self):
        return '<id : {}, version_id : {}, module_name : {}>'.format(self.id, self.version_id,
                                                                     self.module_name)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'version_id': self.version_id,
            'module_name': self.module_name
        }

    @staticmethod
    def sort(elem):
        return elem.module_name


@event.listens_for(OCPIModule.__table__, 'after_create')
def ocpi_model_table_init(*args, **kwargs):
    db_session.add(OCPIModule(id=1, version_id=1, module_name="Tokens"))
    db_session.add(OCPIModule(id=2, version_id=1, module_name="Credentials"))
    db_session.add(OCPIModule(id=3, version_id=1, module_name="Versions"))
    db_session.add(OCPIModule(id=4, version_id=1, module_name="Cdrs"))
    db_session.add(OCPIModule(id=5, version_id=1, module_name="Tariffs"))
    db_session.add(OCPIModule(id=6, version_id=1, module_name="Sessions"))
    db_session.add(OCPIModule(id=7, version_id=1, module_name="Commands"))
    db_session.add(OCPIModule(id=8, version_id=1, module_name="Locations"))
    db_session.commit()
