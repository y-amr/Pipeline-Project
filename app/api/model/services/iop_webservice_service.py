from app.api.model.objects.iop_webservice import IOPWebservice
from app.api.model.objects.ocpi_module import OCPIModule
from app.api.model.objects.ocpi_version import OCPIVersion


class IOPWebserviceService:
    # Return an IOPWebservice
    @staticmethod
    def get_iop_webservice_by_ocpiversion_name_type(ocpiversion, name, ws_type):
        return IOPWebservice.query.join(OCPIModule).join(OCPIVersion).filter(
            OCPIVersion.version_name == ocpiversion).filter(IOPWebservice.webservice_name == name).filter(IOPWebservice.type == ws_type).one()

    @staticmethod
    def get_iop_webservices_by_module_role_type(module_id, role_id, type_id):
        return IOPWebservice.query.filter_by(module_id=module_id,
                                      role_id=role_id,
                                      type=type_id, IOPImplement=True)

    @staticmethod
    def get_iop_webservice_by_id(iop_webservice_id):
        return IOPWebservice.query.filter(
            IOPWebservice.webservice_id == iop_webservice_id).one()
