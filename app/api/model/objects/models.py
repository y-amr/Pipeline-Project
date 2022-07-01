# from sqlalchemy.orm import relationship
# from app.api.model import db
# from app.api.model import IOPWebservice
# from app.api.model import OCPIModule
# from app.api.model.objects.ocpi_role import OCPIRole
# from app.api.model.objects.ocpi_version import OCPIVersion
#
#
# class OCPIReqResp(db.Model):
#     ocpi_req_resp_id = db.Column(db.Integer, primary_key=True)
#     header = db.Column(db.String)
#     body = db.Column(db.String)
#     req_resp_type = db.Column(db.Integer)  # 1 : request, 2 : response
#     REQUEST_TYPE = 1
#     RESPONSE_TYPE = 2
#
#     @property
#     def serialize(self):
#         """Return object data in easily serializable format"""
#         return {
#             'ocpi_req_resp_id': self.ocpi_req_resp_id,
#             'header': self.header,
#             'body': self.body,
#             'req_resp_type': self.req_resp_type
#         }
#
#
# # Reporting des tests
#
#
# class OCPIRequest(db.Model):
#     ocpi_request_id = db.Column(db.Integer, primary_key=True)
#     webservice_id = db.Column(db.Integer, db.ForeignKey(IOPWebservice.webservice_id))
#     url = db.Column(db.String)
#     request_id = db.Column(db.Integer, db.ForeignKey(OCPIReqResp.ocpi_req_resp_id))
#     response_id = db.Column(db.Integer, db.ForeignKey(OCPIReqResp.ocpi_req_resp_id))
#     date_request = db.Column(db.DateTime)
#     verb = db.Column(db.String)
#     response_time = db.Column(db.Integer)
#     http_code = db.Column(db.String)
#     result = db.Column(db.Integer)  # 0 : Ok, 1 : Warning, 2 : Error
#     request = relationship(OCPIReqResp, primaryjoin=request_id == OCPIReqResp.ocpi_req_resp_id, cascade="save-update",
#                            lazy="joined")
#     response = relationship(OCPIReqResp, primaryjoin=response_id == OCPIReqResp.ocpi_req_resp_id, cascade="save-update",
#                             lazy="joined")
#     webService = relationship(IOPWebservice, primaryjoin=webservice_id == IOPWebservice.webservice_id, lazy="joined")
#
#     @property
#     def serialize(self):
#         """Return object data in easily serializable format"""
#         return {
#             'ocpi_request_id': self.ocpi_request_id,
#             'webService': (self.webService.serialize if self.webService is not None else None),
#             'url': self.url,
#             'request': (self.request.serialize if self.request is not None else None),
#             'response': (self.response.serialize if self.response is not None else None),
#             'date_request': self.date_request,
#             'verb': self.verb,
#             'response_time': self.response_time,
#             'http_code': self.http_code,
#             'result': self.result
#         }
#
#
# # Tests de la requête
# class TestsSurRequete(db.Model):
#     test_id = db.Column(db.Integer, primary_key=True)
#
#
# def __init__():
#     db.create_all()
#     OCPIRole.ocpi_role_table_init()
#     OCPIVersion.ocpi_version_table_init()
#     OCPIModule.ocpi_model_table_init()
#     IOPWebservice.iop_webservice_table_init()
