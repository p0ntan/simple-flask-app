"""
Blueprint for api route /user
"""

from flask import Blueprint
from src.controllers.controller_repository import ControllerRepository

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/users")
user_controller = ControllerRepository().get_user_controller()

# Create new user
user_blueprint.route("", methods=["POST"])(user_controller.create)

# Log in
user_blueprint.route("/login", methods=["POST"])(user_controller.login)

# For single user
user_blueprint.route("/<id_num>", methods=["GET"])(user_controller.get_one)
user_blueprint.route("/<id_num>", methods=["PUT"])(user_controller.update)
user_blueprint.route("/<id_num>", methods=["DELETE"])(user_controller.delete)
user_blueprint.route("/<id_num>/image", methods=["POST"])(user_controller.upload_image)
