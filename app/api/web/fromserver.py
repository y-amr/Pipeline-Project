from datetime import datetime

from flask import make_response, jsonify, request

from . import web_api


def shutdown_server():
    func = request.environ.get('werkzeug.web.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# API pour récupérer les requêtes venant du serveur
# @web_api.route("/post", methods=['POST'])
# def recuperation_json():
#     json_post = {"status_code": 1000,
#                  "status_message": "Transmission complete",
#                  "timestamp": "{}{}".format(datetime.utcnow().isoformat(sep='T', timespec='seconds'), "Z")}
#     print(request.query_string)
#     print(request.args.get("method",""))
#     print(request.args.get('endpoint'))
#     print(request.args.get('tokenid'))
#     print(request.args.get('country_code'))
#     print(request.args.get('party_id'))
#     print(request.args.get('repetition'))
#     request_type = request.args.get("method")
#     if request_type == "POST":
#         if int(request.args.get('repetition')) > 0:
#             multi_generation_token(int(request.args.get('repetition')), request.args.get('endpoint'), request.args.get('tokenid'), request.args.get('country_code'), request.args.get('party_id'))
#         else:
#             multi_generation_token(1, request.args.get('endpoint'), request.args.get('tokenid'), request.args.get('country_code'), request.args.get('party_id'))
#     #return;
#     return make_response(jsonify(json_post))
#
# @web_api.route("/shutdown", methods=['POST'])
# def shutdown():
#     return shutdown_server()