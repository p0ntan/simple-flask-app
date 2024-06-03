"""
Blueprint for api route /user
"""
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.controllers.controller_repository import ControllerRepository
from src.errors.customerrors import NoDataException, KeyUnmutableException
from src.utils.response_helper import ResponseHelper

r_helper = ResponseHelper()
user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/user")
uc_instance = ControllerRepository().get_user_controller()


@user_blueprint.route("/", methods=["GET", "POST"])
def index():
  """ Get all users or create new. """
  try:
    # TODO Remove this ? When will this be used?
    if request.method == "GET":
      data = uc_instance.get_all()
      response, status = r_helper.success_response(data)
    elif request.method == "POST":
      result = uc_instance.create(request.json)
      response, status = r_helper.success_response(result, message="New user added.", status=201)
  except Exception as err:
    response, status = r_helper.unkown_error(details=f"{err}")

  return jsonify(response), status


@user_blueprint.route("/<id_num>", methods=["GET", "PUT"])
def single_user(id_num):
  """ Get info from one user. """
  try:
    if request.method == "GET":
      data = uc_instance.get_one(id_num)
      response, status = r_helper.success_response(data)
    elif request.method == "PUT":
      uc_instance.update(id_num, request.json)
      response, status = r_helper.success_response(message="User updated.")
  except (NoDataException, KeyUnmutableException) as err:
    response, status = r_helper.error_response(err.status, details=f"{err}")
  except Exception as err:
    response, status = r_helper.unkown_error(details=f"{err}")

  return jsonify(response), status
