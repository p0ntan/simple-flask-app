"""
Blueprint for api route /post
"""
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.controllers.controller_repository import ControllerRepository
from src.errors.customerrors import NoDataException, KeyUnmutableException
from src.utils.response_helper import ResponseHelper

r_helper = ResponseHelper()
post_blueprint = Blueprint('post_blueprint', __name__, url_prefix="/post")
pc_instance = ControllerRepository().get_post_controller()


@post_blueprint.route("/", methods=["POST"])
def index():
  """ Create new post. """
  try:
    if request.method == "POST":
      result = pc_instance.create(request.json)
      response, status = r_helper.success_response(result, message="New post added.", status=201)
  except Exception as err:
    response, status = r_helper.unkown_error(details=f"{err}")

  return jsonify(response), status


@post_blueprint.route("/<id_num>", methods=["GET", "PUT"])
def single_post(id_num):
  """ Get info from one post. """
  try:
    if request.method == "GET":
      data = pc_instance.get_one(id_num)
      response, status = r_helper.success_response(data)
    elif request.method == "PUT":
      pc_instance.update(id_num, request.json)
      response, status = r_helper.success_response(message="Post updated.")
  except (NoDataException, KeyUnmutableException) as err:
    response, status = r_helper.error_response(err.status, details=f"{err}")
  except Exception as err:
    response, status = r_helper.unkown_error(details=f"{err}")

  return jsonify(response), status
