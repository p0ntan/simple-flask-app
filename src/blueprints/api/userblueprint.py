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


@user_blueprint.route("/all", methods=["GET"])
def get_users():
  # TODO Remove this ? When will this be used?
  """ Get all users. """
  try:
    data = uc_instance.get_all()
    response = r_helper.success_response(data)
    status = 200
  except Exception as err:
    response = r_helper.unkown_error(details=f"{err}")
    status = 500

  return jsonify(response), status


@user_blueprint.route("/<id_num>", methods=["GET"])
def get_user(id_num):
  """ Get info from one user. """
  try:
    data = uc_instance.get_one(id_num)
    response = r_helper.success_response(data)
    status = 200
  except NoDataException as err:
    response = r_helper.error_response(err.status, details=f"{err}")
    status = err.status
  except Exception as err:
    response = r_helper.unkown_error(details=f"{err}")
    status = 500

  return jsonify(response), status


@user_blueprint.route("/<id_num>", methods=["PUT"])
def update_user(id_num):
  """ Update a user. """
  try:
    data = request.json
    uc_instance.update(id_num, data)
    response = r_helper.success_response(message="User updated.")
    status = 200
  except (NoDataException, KeyUnmutableException) as err:
    response = r_helper.error_response(err.status, details=f"{err}")
    status = err.status
  except Exception as err:
    response = r_helper.unkown_error(details=f"{err}")
    status = 500

  return jsonify(response), status


@user_blueprint.route("/create", methods=["POST"])
def create_user():
  """ Create a user. """
  try:
    data = request.json
    result = uc_instance.create(data)
    response = r_helper.success_response(result, message="New user added.")
    status = 200
  except Exception as err:
    response = r_helper.unkown_error(details=f"{err}")
    status = 500

  return jsonify(response), status
