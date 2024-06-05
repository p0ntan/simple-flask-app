"""
TopicController is for handling all calls to database regarding topics.
"""
from flask import jsonify, request
from src.controllers.controller import Controller
from src.utils.dao import DAO
from src.utils.postdao import PostDAO
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import NoDataException, KeyUnmutableException

r_helper = ResponseHelper()


class TopicController(Controller):
  """TopicController handles all dataaccess for topics."""
  def __init__(self, topic_dao: DAO, post_dao: PostDAO):
    super().__init__(dao=topic_dao)
    self._post_dao = post_dao

  def root(self) -> tuple[dict, int]:
    """Controller for root route."""
    try:
      if request.method == "POST":
        result = self.create(request.json)
        response, status = r_helper.success_response(result, message="New topic added.", status=201)
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status
  
  def single_topic(self, id_num = int) -> tuple[dict, int]:
    """Controller for single topic route

    Parameters:
      id_num(int):  id for topic

    Returns:
      response, status
    """
    try:
      if request.method == "GET":
        data = self.get_one(id_num)
        response, status = r_helper.success_response(data)
      elif request.method == "PUT":
        self.update(id_num, request.json)
        response, status = r_helper.success_response(message="Post updated.")
    except (NoDataException, KeyUnmutableException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def topic_with_posts(self, id_num: int, page_num: int = 0) -> tuple[dict, int]:
    """When using route for single topic

    Parameters:
      id_num(int):    id for topic
      page_num(int):  pagenumber, default is 0 which is first page. Each page has 10 posts.

    Returns:
      tuple[response, status]
    """
    try:
      if request.method == "GET":
        data = self._post_dao.get_posts_and_topic(id_num, page_num)

        response, status = r_helper.success_response(data)
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

