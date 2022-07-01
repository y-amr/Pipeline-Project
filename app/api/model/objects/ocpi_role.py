from sqlalchemy import Column, String, Integer, event

from app.Base import Base, db_session


class OCPIRole(Base):
    __tablename__ = "ocpi_role"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(128))

    # Creation des roles CPO/eMSP
    @staticmethod
    def __repr__(self):
        return '<Id : {}, Nom : {}>'.format(self.id, self.role_name)


@event.listens_for(OCPIRole.__table__, 'after_create')
def ocpi_role_table_init(*args, **kwargs):
    db_session.add(OCPIRole(id=1, role_name="cpo"))
    db_session.add(OCPIRole(id=2, role_name="emsp"))
    db_session.commit()
