"""
Blueprint for api route /topic
"""
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.controllers.controller_repository import ControllerRepository
from src.errors.customerrors import NoDataException, KeyUnmutableException
from src.utils.response_helper import ResponseHelper

r_helper = ResponseHelper()
topic_blueprint = Blueprint("topic_blueprint", __name__, url_prefix="/topic")
topic_controller = ControllerRepository().get_topic_controller()

topic_blueprint.route("/", methods=["POST"])(topic_controller.root)
topic_blueprint.route("/<id_num>", methods=["GET", "PUT"])(topic_controller.singel_topic)

# Middleware
def before_request_middleware():
    auth = dict(request.headers)
    if "Authorization" not in auth:
      response, status = r_helper.error_response(403, details="Shouldn't woork!")
      return jsonify(response), status
    
    print(auth["Authorization"][8:])

# Lägg till middleware till api_blueprint
# topic_blueprint.before_request(before_request_middleware)
