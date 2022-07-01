import logging

from flask import render_template, request, jsonify, session
from app import app
from app.authentication import requires_auth
from . import web_unittests_api
from ...model.objects.ocpi_module import OCPIModule
from ...model.objects.ocpi_role import OCPIRole
from ...model.objects.ocpi_version import OCPIVersion
from ...model.objects.parameter import Parameter
from ...model.services.iop_webservice_service import IOPWebserviceService
from ...model.services.parameter_service import ParameterService
from ...model.services.test_report_service import TestReportService
from ...utils.two_one_one.constants import Constants


@web_unittests_api.route("/webservices", methods=['GET'])
@requires_auth
def get_ocpi_webservices():
    return jsonify(json_list=[i.serialize for i in
                              IOPWebserviceService.get_iop_webservices_by_module_role_type(
                                  module_id=request.args.get('module_id'), role_id=request.args.get('role_id'),
                                  type_id=request.args.get('type'))])


@web_unittests_api.route("/webservice-form", methods=['GET'])
@requires_auth
def get_webservice_form():
    # Recuperation du WS
    iop_ws = IOPWebserviceService.get_iop_webservice_by_id(int(request.args.get('webservice_id')))
    # Recuperation des parametres lies a l utilisateur
    parameters = ParameterService.get_all_parameters_by_userid(session['profile']['user_id'])
    # Recuperation de l'URL du serveur

    return render_template(
        "webservice-forms/two_one_one/" + iop_ws.ocpi_module.module_name + "/" + iop_ws.webservice_name + "_" + iop_ws.ocpi_role.role_name + "_" + iop_ws.type + ".html",
        parameters=parameters, constants=Constants())


@web_unittests_api.route("/ocpimodules", methods=['GET'])
@requires_auth
def get_ocpi_modules():
    return jsonify(
        json_list=[i.serialize for i in sorted(OCPIModule.query.filter_by(version_id=request.args.get('ocpi_version')),
                                               key=OCPIModule.sort)])


@web_unittests_api.route("/getIOPRequests", methods=['GET'])
def get_IOP_requests():
    # A l init, ttes requetes arrivees dans les 5 dernieres minutes
    if request.args.get('lastRequestId') is not None:
        return jsonify(maxId=TestReportService.get_test_report_max_id_by_userid("IOP"),
                       json_list=[i.printable_form for i in
                                  TestReportService.get_test_report_from_index_by_userid(
                                      int(request.args.get(
                                          'lastRequestId')), "IOP")])
    return jsonify(maxId=TestReportService.get_test_report_max_id_by_userid("IOP"),
                   json_list=[i.printable_form for i in
                              TestReportService.get_test_report_from_index_by_userid(0, "IOP")])


@web_unittests_api.route("/getProcessingRequests", methods=['GET'])
def get_non_reg_processing():
    # A l init, ttes requetes arrivees dans les 5 dernieres minutes
    if request.args.get('lastRequestId') is not None:
        return jsonify(maxId=TestReportService.get_processing_nr_max_id_by_env_id("IOP-PP"),
                       json_list=[i.printable_form for i in
                                  TestReportService.get_processing_nr_from_index_by_env(
                                      int(request.args.get(
                                          'lastRequestId')), "IOP-PP")])
    return jsonify(maxId=TestReportService.get_processing_nr_max_id_by_env_id("IOP-PP"),
                   json_list=[i.printable_form for i in
                              TestReportService.get_processing_nr_from_index_by_env(0, "IOP-PP")])


@web_unittests_api.route("/getRequests", methods=['GET'])
@requires_auth
def get_requests():
    # A l init, ttes requetes arrivees dans les 5 dernieres minutes
    if request.args.get('lastRequestId') is not None:
        return jsonify(maxId=TestReportService.get_test_report_max_id_by_userid(session['profile']['user_id']),
                       json_list=[i.printable_form for i in
                                  TestReportService.get_test_report_from_index_by_userid(
                                      int(request.args.get(
                                          'lastRequestId')), session['profile']['user_id'])])
    return jsonify(maxId=TestReportService.get_test_report_max_id_by_userid(session['profile']['user_id']),
                   json_list=[i.printable_form for i in
                              TestReportService.get_test_report_from_index_by_userid(0, session['profile']['user_id'])])


@web_unittests_api.route("/setWebserviceParameters", methods=['POST'])
@requires_auth
def set_webservice_parameters():
    json_parameters = request.json
    # Enregistrement de chacun des parametres
    parameter_list = []
    for key, value in json_parameters.items():
        if value is not '':
            parameter_list.append(Parameter(key=key, value=value, user_id=session['profile']['user_id']))
    ParameterService.save_parameters(parameter_list)
    return jsonify(status="Success")


@web_unittests_api.route("", methods=['GET'])
@requires_auth
def get_ocpi_versions():
    logging.debug('Recuperation des versions d\'OCPI')
    versions = OCPIVersion.query.all()
    roles = OCPIRole.query.all()
    return render_template("unit-tests/index.html", title='Unitary Tests', ocpi_versions=versions, roles=roles,
                           version=app.config['VERSION'])
