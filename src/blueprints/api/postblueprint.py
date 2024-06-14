"""
Blueprint for api route /post
"""

from flask import Blueprint
from src.controllers.controller_repository import ControllerRepository

post_blueprint = Blueprint("post_blueprint", __name__, url_prefix="/posts")
post_controller = ControllerRepository().get_post_controller()

# Create new post
post_blueprint.route("", methods=["POST"])(post_controller.create)

# For single post
post_blueprint.route("/<id_num>", methods=["GET"])(post_controller.get_one)
post_blueprint.route("/<id_num>", methods=["PUT"])(post_controller.update)
post_blueprint.route("/<id_num>", methods=["DELETE"])(post_controller.delete)
