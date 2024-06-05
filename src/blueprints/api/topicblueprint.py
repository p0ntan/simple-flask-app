"""
Blueprint for api route /topic
"""
from flask import Blueprint
from src.controllers.controller_repository import ControllerRepository

topic_blueprint = Blueprint("topic_blueprint", __name__, url_prefix="/topics")
topic_controller = ControllerRepository().get_topic_controller()

# Create new topic
topic_blueprint.route("/", methods=["POST"])(topic_controller.root)

# For single topic
topic_blueprint.route("/<id_num>", methods=["GET", "PUT"])(topic_controller.single_topic)
topic_blueprint.route("/<id_num>/page/", methods=["GET"])(topic_controller.topic_with_posts)
topic_blueprint.route("/<id_num>/page/<page_num>", methods=["GET"])(topic_controller.topic_with_posts)
