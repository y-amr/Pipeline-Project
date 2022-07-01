from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship

from app.Base import Base, db_session
from app.api.model.objects.ocpi_module import OCPIModule
from app.api.model.objects.ocpi_role import OCPIRole


class IOPWebservice(Base):
    # Tokens module
    WS_NAME_GET_emsp_Tokens = "GET_emsp_Tokens"
    WS_NAME_PUT_cpo_Tokens = "PUT_cpo_Tokens"
    WS_NAME_PATCH_cpo_Tokens = "PATCH_cpo_Tokens"
    WS_NAME_POST_emsp_Tokens_authorize = "POST_emsp_Tokens-authorize"
    WS_NAME_GET_cpo_Tokens = "GET_cpo_Tokens"
    # Versions endpoint
    WS_NAME_GET_emsp_versions = "GET_emsp_versions"
    WS_NAME_GET_emsp_version_details = "GET_emsp_version-details"
    WS_NAME_POST_emsp_credentials = "POST_emsp_credentials"
    WS_NAME_PUT_emsp_credentials = "PUT_emsp_credentials"
    WS_NAME_DELETE_emsp_credentials = "DELETE_emsp_credentials"
    WS_NAME_GET_emsp_credentials = "GET_emsp_credentials"
    WS_NAME_GET_cpo_versions = "GET_cpo_versions"
    WS_NAME_GET_cpo_version_details = "GET_cpo_version-details"
    WS_NAME_POST_cpo_credentials = "POST_cpo_credentials"
    WS_NAME_PUT_cpo_credentials = "PUT_cpo_credentials"
    WS_NAME_DELETE_cpo_credentials = "DELETE_cpo_credentials"
    WS_NAME_GET_cpo_credentials = "GET_cpo_credentials"
    # CDR module
    WS_NAME_POST_emsp_CDRs = "POST_emsp_CDRs"
    WS_NAME_GET_emsp_CDRs = "GET_emsp_CDRs"
    WS_NAME_GET_cpo_CDRs = "GET_cpo_CDRs"
    # Sessions module
    WS_NAME_PUT_emsp_Sessions = "PUT_emsp_Sessions"
    WS_NAME_PATCH_emsp_Sessions = "PATCH_emsp_Sessions"
    WS_NAME_GET_cpo_Sessions = "GET_cpo_Sessions"
    WS_NAME_GET_emsp_Sessions = "GET_emsp_Sessions"
    # Commands module
    WS_NAME_POST_cpo_Commands_START_SESSION = "POST_cpo_Commands_START_SESSION"
    WS_NAME_POST_cpo_Commands_STOP_SESSION = "POST_cpo_Commands_STOP_SESSION"
    WS_NAME_POST_cpo_Commands_RESERVE_NOW = "POST_cpo_Commands_RESERVE_NOW"
    WS_NAME_POST_cpo_Commands_UNLOCK_CONNECTOR = "POST_cpo_Commands_UNLOCK_CONNECTOR"
    WS_NAME_POST_emsp_Commands_CALLBACK = "POST_emsp_Commands_CALLBACK"
    # Locations module
    WS_NAME_PUT_emsp_Locations = "PUT_emsp_Locations"
    WS_NAME_PATCH_emsp_Locations = "PATCH_emsp_Locations"
    WS_NAME_GET_cpo_Locations = "GET_cpo_Locations"
    WS_NAME_GET_emsp_Locations = "GET_emsp_Locations"
    # Tariffs module
    WS_NAME_GET_cpo_Tariffs = "GET_cpo_Tariffs"
    WS_NAME_GET_emsp_Tariffs = "GET_emsp_Tariffs"
    WS_NAME_PATCH_emsp_Tariffs = "PATCH_emsp_Tariffs"
    WS_NAME_PUT_emsp_Tariffs = "PUT_emsp_Tariffs"
    WS_NAME_DELETE_emsp_Tariffs = "DELETE_emsp_Tariffs"

    __tablename__ = "iop_webservice"
    webservice_id = Column(Integer, primary_key=True)
    webservice_name = Column(String(128))
    module_id = Column(Integer, ForeignKey(OCPIModule.id))
    role_id = Column(Integer, ForeignKey(OCPIRole.id))
    type = Column(String(1))  # F = FromServer ; T = ToServer
    IOPImplement = Column(Boolean)  # True = Implemented by IOP ; False = Not implemented by IOP
    TYPE_FROMSERVER = 'F'
    TYPE_TOSERVER = 'T'
    ocpi_module = relationship(OCPIModule)
    ocpi_role = relationship(OCPIRole)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'webservice_id': self.webservice_id,
            'webservice_name': self.webservice_name,
            'module_id': self.module_id,
            'role_id': self.role_id,
            'type': self.type,
            'IOPImplement': self.IOPImplement
        }


@event.listens_for(IOPWebservice.__table__, 'after_create')
def iop_webservice_table_init(*args, **kwargs):
    # Module Tokens, role CPO
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_Tokens, module_id=1, role_id=1, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_cpo_Tokens, module_id=1, role_id=1, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PATCH_cpo_Tokens, module_id=1, role_id=1, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_Tokens, module_id=1, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_emsp_Tokens_authorize, module_id=1, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER, IOPImplement=1))

    # Module Tokens, role emsp
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_Tokens, module_id=1, role_id=2, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_cpo_Tokens, module_id=1, role_id=2, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PATCH_cpo_Tokens, module_id=1, role_id=2, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_emsp_Tokens_authorize, module_id=1, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_Tokens, module_id=1, role_id=2, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))

    # Module Credentials, role CPO
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_versions, module_id=3, role_id=1, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_version_details, module_id=3, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER, IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_versions, module_id=3, role_id=1, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_version_details, module_id=3, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_credentials, module_id=2, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_emsp_credentials, module_id=2, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_cpo_credentials, module_id=2, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_emsp_credentials, module_id=2, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_credentials, module_id=2, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_DELETE_cpo_credentials, module_id=2, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_credentials, module_id=2, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_DELETE_emsp_credentials, module_id=2, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=0))

    # Module Credentials, role emsp
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_versions, module_id=3, role_id=2, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_version_details, module_id=3, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER, IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_versions, module_id=3, role_id=2, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_version_details, module_id=3, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_emsp_credentials, module_id=2, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_credentials, module_id=2, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_emsp_credentials, module_id=2, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_cpo_credentials, module_id=2, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_credentials, module_id=2, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_DELETE_emsp_credentials, module_id=2, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_credentials, module_id=2, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_DELETE_cpo_credentials, module_id=2, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=0))

    # Module Cdrs, role CPO
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_emsp_CDRs, module_id=4, role_id=1, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_CDRs, module_id=4, role_id=1, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_CDRs, module_id=4, role_id=1, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))

    # Module Cdrs, role emsp
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_emsp_CDRs, module_id=4, role_id=2, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_CDRs, module_id=4, role_id=2, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_CDRs, module_id=4, role_id=2, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))

    # Module Sessions, role CPO
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_emsp_Sessions, module_id=6, role_id=1, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PATCH_emsp_Sessions, module_id=6, role_id=1, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_Sessions, module_id=6, role_id=1, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_Sessions, module_id=6, role_id=1, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))

    # Module Sessions, role emsp
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_emsp_Sessions, module_id=6, role_id=2, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PATCH_emsp_Sessions, module_id=6, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER, IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_Sessions, module_id=6, role_id=2, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_Sessions, module_id=6, role_id=2, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))

    # Module Commands, role CPO
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_Commands_START_SESSION, module_id=7, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER, IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_Commands_STOP_SESSION, module_id=7, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER, IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_Commands_RESERVE_NOW, module_id=7, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER, IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_Commands_UNLOCK_CONNECTOR, module_id=7, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER, IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_emsp_Commands_CALLBACK, module_id=7, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER, IOPImplement=1))

    # Module Commands, role emsp
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_Commands_START_SESSION, module_id=7, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_Commands_STOP_SESSION, module_id=7, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_Commands_RESERVE_NOW, module_id=7, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_cpo_Commands_UNLOCK_CONNECTOR, module_id=7, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=0))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_POST_emsp_Commands_CALLBACK, module_id=7, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))

    # Module Locations, role CPO
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_emsp_Locations, module_id=8, role_id=1, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PATCH_emsp_Locations, module_id=8, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_Locations, module_id=8, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_Locations, module_id=8, role_id=1, type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))

    # Module Locations, role emsp
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_emsp_Locations, module_id=8, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PATCH_emsp_Locations, module_id=8, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_Locations, module_id=8, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_Locations, module_id=8, role_id=2, type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))

    # Module Tariffs, role CPO
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_emsp_Tariffs, module_id=5, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PATCH_emsp_Tariffs, module_id=5, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_Tariffs, module_id=5, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_DELETE_emsp_Tariffs, module_id=5, role_id=1,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_Tariffs, module_id=5, role_id=1,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))

    # Module Tariffs, role emsp
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PUT_emsp_Tariffs, module_id=5, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_PATCH_emsp_Tariffs, module_id=5, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_emsp_Tariffs, module_id=5, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_DELETE_emsp_Tariffs, module_id=5, role_id=2,
                      type=IOPWebservice.TYPE_FROMSERVER,
                      IOPImplement=1))
    db_session.add(
        IOPWebservice(webservice_name=IOPWebservice.WS_NAME_GET_cpo_Tariffs, module_id=5, role_id=2,
                      type=IOPWebservice.TYPE_TOSERVER,
                      IOPImplement=1))

    db_session.commit()
