import json

import requests
from flask import request, make_response, jsonify

from app.api.server.two_one_one.cpo import ocpi_cpo_211

# Transformer une payload json en données manipulables pour python


# class Payload(object):
#     def __init__(self, j):
#         self.__dict__ = json.loads(j)
#
#
# @ocpi_cpo_211.route("/credentials", methods=['PUT'])
# def send_versions():
#     # Verification de tous les champs
#     data = Payload(request.data)
#     NewToken = data.token
#     url = data.url
#     partyId = data.party_id
#     countryCode = data.country_code
#
#     HeadersNewRequest = {'Token': 'Token ' + NewToken}
#     response = Payload(requests.get(url, headers=HeadersNewRequest).content)
#     for versionsOCPI in response.data:
#         if versionsOCPI.get('version', '') == "2.1.1":
#             urlDetails = versionsOCPI.get('url', '')
#     versionDetailsData = Payload(requests.get(urlDetails, headers=HeadersNewRequest).content)
#     data = jsonify(versionDetailsData.data).data
#     endpoints = Payload(data)
#     for versionsDetails in endpoints.endpoints:
#         if versionsDetails.get('identifier', '') == "commands":
#             commands = versionsDetails.get('url', '')
#         elif versionsDetails.get('identifier', '') == "cdrs":
#             cdrs = versionsDetails.get('url', '')
#         elif versionsDetails.get('identifier', '') == "tokens":
#             tokens = versionsDetails.get('url', '')
#         elif versionsDetails.get('identifier', '') == "sessions":
#             sessions = versionsDetails.get('url', '')
#         elif versionsDetails.get('identifier', '') == "credentials":
#             credentials = versionsDetails.get('url', '')
#     print("commands = " + commands)
#     print("cdrs = " + cdrs)
#     print("tokens = " + tokens)
#     print("sessions = " + sessions)
#     print("credentials = " + credentials)
#
#     response = make_response()
#     return response
