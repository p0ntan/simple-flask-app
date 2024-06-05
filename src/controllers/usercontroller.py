"""
Usercontroller is for handling all calls to database regarding users.
"""
from flask import jsonify, request
from src.controllers.controller import Controller
from src.utils.dao import DAO
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import NoDataException, KeyUnmutableException

r_helper = ResponseHelper()

class UserController(Controller):
  """ UserController handles all dataaccess for users. """
  def __init__(self, user_dao: DAO):
    super().__init__(dao=user_dao)

  def root(self) -> tuple[dict, int]:
    """Controller for root route."""
    try:
      if request.method == "POST":
        result = self.create(request.json)
        response, status = r_helper.success_response(result, message="New user added.", status=201)
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def single_user(self, id_num = int) -> tuple[dict, int]:
    """Controller for single user route

    Parameters:
      id_num(int):  id for user

    Returns:
      response, status
    """
    try:
      if request.method == "GET":
        data = self.get_one(id_num)
        response, status = r_helper.success_response(data)
      elif request.method == "PUT":
        self.update(id_num, request.json)
        response, status = r_helper.success_response(message="User updated.")
    except (NoDataException, KeyUnmutableException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status