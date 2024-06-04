"""
Blueprint for api route /post
"""
from flask import Blueprint
from src.controllers.controller_repository import ControllerRepository

post_blueprint = Blueprint('post_blueprint', __name__, url_prefix="/post")
post_controller = ControllerRepository().get_post_controller()

post_blueprint.route("/", methods=["POST"])(post_controller.root)
post_blueprint.route("/<id_num>", methods=["GET", "PUT"])(post_controller.single_post)
