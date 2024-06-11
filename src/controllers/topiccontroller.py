"""
TopicController is for handling all calls to database regarding topics.
"""
from flask import jsonify, request, Response
from src.controllers.basecontroller import Controller
from src.services.topic_service import TopicService
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import NoDataException, KeyUnmutableException, InputInvalidException, UnauthorizedException

r_helper = ResponseHelper()


class TopicController(Controller):
  """TopicController handles all dataaccess for topics."""

  def __init__(self, service: TopicService):
    """Initializes the TopicController class.
    
    Args:
      service (TopicService): An instance of the TopicService class.
    """
    self._service = service

  def create(self) -> tuple[Response, int]:
    """Controller for root route.
  
    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      input_data = request.json

      if input_data is None:
        raise InputInvalidException("Missing input input data.")

      result = self._service.create(input_data)  # TODO get id from token or other way
      response, status = r_helper.success_response(result, message="New topic added.", status=201)

    except (InputInvalidException, NoDataException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def get_one(self, id_num: int) -> tuple[Response, int]:
    """Controller getting one topic, including creator (user).

    Args:
      id_num(int):  id for topic

    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      result = self._service.get_by_id(id_num)
      response, status = r_helper.success_response(result)
    except (NoDataException, KeyUnmutableException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def update(self, id_num: int) -> tuple[Response, int]:
    """Controller for updating a topic.

    Args:
      id_num(int):  id for topic

    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      input_data = request.json

      if input_data is None:
        raise InputInvalidException("Missing input data.")

      result = self._service.update(id_num, input_data)
      response, status = r_helper.success_response(result)
    except (NoDataException, UnauthorizedException) as err:
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
      data = self._service.get_topic_posts_users(id_num, page_num)

      response, status = r_helper.success_response(data)
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def delete(self, id_num: int) -> tuple[Response, int]:
    """Deletes a topic.

    Args:
      id_num (int): The id of the topic.

    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      success = self._service.delete(id_num)
      message, status = ("Topic deleted.", 200) if success else ("Topic not deleted.", 202)

      response, status = r_helper.success_response(message=message, status=status)
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status
