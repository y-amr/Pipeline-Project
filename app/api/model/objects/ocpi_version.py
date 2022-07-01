from sqlalchemy import Column, Integer, String, event

from app.Base import Base, db_session


class OCPIVersion(Base):
    two_one_one = "2.1.1"
    __tablename__ = "ocpi_version"
    id = Column(Integer, primary_key=True)
    version_name = Column(String(128))


@event.listens_for(OCPIVersion.__table__, 'after_create')
def ocpi_version_table_init(*args, **kwargs):
    db_session.add(OCPIVersion(id=1, version_name=OCPIVersion.two_one_one))
    db_session.commit()
