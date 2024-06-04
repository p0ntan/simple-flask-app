"""
Blueprint for api route /topic
"""
from flask import Blueprint
from src.controllers.controller_repository import ControllerRepository

topic_blueprint = Blueprint("topic_blueprint", __name__, url_prefix="/topic")
topic_controller = ControllerRepository().get_topic_controller()

topic_blueprint.route("/", methods=["POST"])(topic_controller.root)
topic_blueprint.route("/<id_num>", methods=["GET", "PUT"])(topic_controller.singel_topic)
