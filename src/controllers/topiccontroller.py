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

  def singel_topic(self, id_num = int) -> tuple[dict, int]:
    """When using route for single topic

    Parameters:
      id_num(int):  id for topic

    Returns:
      tuple[response, status]
    """
    try:
      if request.method == "GET":
        page = request.args.get('page', 0)
        data = self._post_dao.get_posts_and_topic(id_num, int(page))

        response, status = r_helper.success_response(data)
      elif request.method == "PUT":
        self.update(id_num, request.json)
        response, status = r_helper.success_response(message="Topic updated.")
    except (NoDataException, KeyUnmutableException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

