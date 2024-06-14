"""
Blueprint for api route /topic
"""

from flask import Blueprint
from src.controllers.controller_repository import ControllerRepository

topic_blueprint = Blueprint("topic_blueprint", __name__, url_prefix="/topics")
topic_controller = ControllerRepository().get_topic_controller()

# Create new topic
topic_blueprint.route("/", methods=["POST"])(topic_controller.create)

# For single topic
topic_blueprint.route("/<id_num>", methods=["GET"])(topic_controller.get_one)
topic_blueprint.route("/<id_num>", methods=["PUT"])(topic_controller.update)
topic_blueprint.route("/<id_num>", methods=["DELETE"])(topic_controller.delete)
topic_blueprint.route("/<id_num>/page/", methods=["GET"])(
    topic_controller.topic_with_posts
)
topic_blueprint.route("/<id_num>/page/<page_num>", methods=["GET"])(
    topic_controller.topic_with_posts
)

# Get latest topics
topic_blueprint.route("/latest", methods=["GET"])(topic_controller.latest_topics)
