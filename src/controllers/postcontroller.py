"""
PostController is for handling all calls to database regarding posts.
"""
from flask import jsonify, request
from src.controllers.controller import Controller
from src.utils.dao import DAO
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import NoDataException, KeyUnmutableException

r_helper = ResponseHelper()


class PostController(Controller):
  """ PostController handles all dataaccess for posts. """
  def __init__(self, post_dao: DAO):
    super().__init__(dao=post_dao)

  def root(self) -> tuple[dict, int]:
    """Controller for root route."""
    try:  
      if request.method == "POST":
        result = self.create(request.json)
        response, status = r_helper.success_response(result, message="New post added.", status=201)
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def single_post(self, id_num = int) -> tuple[dict, int]:
    """Controller for single post route

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
