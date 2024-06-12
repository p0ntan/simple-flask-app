"""
TopicController is for handling all calls to database regarding topics.
"""
from flask import jsonify, request, Response
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.controllers.basecontroller import Controller
from src.services.topic_service import TopicService
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import NoDataException, InputInvalidException, UnauthorizedException

r_helper = ResponseHelper()


class TopicController(Controller):
  """TopicController handles all dataaccess for topics."""

  def __init__(self, service: TopicService, controller_name: str):
    """Initializes the PostController class.

    Args:
      service (PostService): An instance of the PostService class.
      controller_name (str): The name of the controller.
    """
    self._service = service
    self._controller = controller_name

  @jwt_required()
  def create(self) -> tuple[Response, int]:
    """Controller for root route, creating a new topic.
  
    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      input_data = request.json

      if input_data is None:
        raise InputInvalidException("Missing input data.")
      
      current_user = get_jwt_identity()
      result = self._service.create(input_data, current_user)
      response, status = r_helper.success_response(result, message=f"New {self._controller} added.", status=201)

    except (InputInvalidException, NoDataException, UnauthorizedException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def latest_topics(self) -> tuple[Response, int]:
    """Get latest topics, based on what date the topic was created.

    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      data = self._service.get_latest_topics()

      response, status = r_helper.success_response(data)
    except NoDataException as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def topic_with_posts(self, id_num: int, page_num: int = 0) -> tuple[Response, int]:
    """When using route for single topic

    Args:
      id_num(int):    id for topic
      page_num(int):  pagenumber, default is 0 which is first page. Each page has 10 posts.

    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      data = self._service.get_topic_posts_users(id_num, int(page_num))

      response, status = r_helper.success_response(data)
    except NoDataException as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status
