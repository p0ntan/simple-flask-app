"""
Blueprint for api route /user
"""
from flask import Blueprint
from src.controllers.controller_repository import ControllerRepository

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/user")
user_controller = ControllerRepository().get_user_controller()

user_blueprint.route("/", methods=["POST"])(user_controller.root)
user_blueprint.route("/<id_num>", methods=["GET", "PUT"])(user_controller.single_user)
