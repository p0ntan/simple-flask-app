from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin
from src.controllers.controller_repository import ControllerRepository

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/user")

@user_blueprint.route("/all", methods=["GET"])
def get_all():
  # TODO Remove this ? When will this be used?
  """ Get all users. """
  try:
    uc_instance = ControllerRepository().get_user_controller()
    data = uc_instance.get_all()
    return jsonify(data)
  except Exception as err:
    print(err)
    abort(500, "Unknown server error, try again.")

@user_blueprint.route("/<id>", methods=["GET"])
def get_one(id):
  """ Get info from one user. """
  try:
    uc_instance = ControllerRepository().get_user_controller()
    data = uc_instance.get_one(id)
    return jsonify(data)
  except Exception as err:
    print(err)
    abort(500, "Unknown server error, try again.")

@user_blueprint.route("/<id>", methods=["PUT"])
def put_one(id):
  """ Update a user. """
  try:
    uc_instance = ControllerRepository().get_user_controller()
    data = request.json
    result = uc_instance.update(id, data)
    return jsonify({"success": result})
  except Exception as err:
    print(err)
    abort(500, "Unknown server error, try again.")