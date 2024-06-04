"""
Blueprint for api route /topic
"""
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.controllers.controller_repository import ControllerRepository
from src.errors.customerrors import NoDataException, KeyUnmutableException
from src.utils.response_helper import ResponseHelper

r_helper = ResponseHelper()
topic_blueprint = Blueprint('topic_blueprint', __name__, url_prefix="/topic")
tc_instance = ControllerRepository().get_topic_controller()


@topic_blueprint.route("/", methods=["POST"])
def index():
  """ Create new topic. """
  try:
    if request.method == "POST":
      result = tc_instance.create(request.json)
      response, status = r_helper.success_response(result, message="New topic added.", status=201)
  except Exception as err:
    response, status = r_helper.unkown_error(details=f"{err}")

  return jsonify(response), status


@topic_blueprint.route("/<id_num>", methods=["GET", "PUT"])
def single_topic(id_num: int):
  """ Get info from one topic, with posts. """
  try:
    if request.method == "GET":
      page = request.args.get('page', 0)

      data = tc_instance.get_topic_and_posts(id_num, int(page))

      response, status = r_helper.success_response(data)
    elif request.method == "PUT":
      tc_instance.update(id_num, request.json)
      response, status = r_helper.success_response(message="Topic updated.")
  except (NoDataException, KeyUnmutableException) as err:
    response, status = r_helper.error_response(err.status, details=f"{err}")
  except Exception as err:
    response, status = r_helper.unkown_error(details=f"{err}")

  return jsonify(response), status

# Middleware
def before_request_middleware():
    auth = dict(request.headers)
    if "Authorization" not in auth:
      response, status = r_helper.error_response(403, details="Shouldn't woork!")
      return jsonify(response), status
    
    print(auth["Authorization"][8:])

# Lägg till middleware till api_blueprint
# topic_blueprint.before_request(before_request_middleware)
