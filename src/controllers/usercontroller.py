"""
Usercontroller is for handling all calls to database regarding users.
"""
from flask import jsonify, request, Response
from src.controllers.controller import Controller
from src.utils.userdao import UserDAO
from src.utils.response_helper import ResponseHelper
from src.services.user_service import UserService
from src.errors.customerrors import NoDataException, KeyUnmutableException

r_helper = ResponseHelper()
user_dao = UserDAO("user")
user_service = UserService(user_dao)

class UserController(Controller):
  """ UserController handles all dataaccess for users. """
  def __init__(self, user_dao: UserDAO):
    super().__init__(dao=user_dao)

  def root(self) -> tuple[Response, int]:
    """Controller for root route."""
    try:
      if request.method == "POST":
        result = self.create(request.json)
        response, status = r_helper.success_response(result, message="New user added.", status=201)
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def login(self) -> tuple[Response, int]:
    """Controller for root route."""
    try:
      if request.method == "POST":
        result = request.json
        user = user_service.login(result["username"], "ps")

        response, status = r_helper.success_response(user, message="User logged in.", status=200)
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def single_user(self, id_num = int) -> tuple[Response, int]:
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