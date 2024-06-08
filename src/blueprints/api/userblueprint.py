"""
Blueprint for api route /user
"""
from flask import Blueprint
from src.controllers.controller_repository import ControllerRepository

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/users")
user_controller = ControllerRepository().get_user_controller()

user_blueprint.route("/", methods=["POST"])(user_controller.create_user)
user_blueprint.route("/login", methods=["POST"])(user_controller.login)
user_blueprint.route("/<id_num>", methods=["GET", "PUT"])(user_controller.single_user)
