"""
Usercontroller is for handling all calls to database regarding users.
"""
from flask import jsonify, request, Response
from src.controllers.controller import Controller
from src.utils.daos.userdao import UserDAO
from src.utils.response_helper import ResponseHelper
from src.services.user_service import UserService
from src.errors.customerrors import NoDataException, InputInvalidException, KeyUnmutableException

r_helper = ResponseHelper()
user_dao = UserDAO("user")
user_service = UserService(user_dao)

class UserController(Controller):
  """ UserController handles all dataaccess for users. """
  def __init__(self, user_dao: UserDAO):
    super().__init__(dao=user_dao)

  # TODO change to use abstract methods from controller
  def create_user(self) -> tuple[Response, int]:
    """Controller for root route."""
    try:
      input_data = request.json

      if input_data is None or "username" not in input_data:
        raise InputInvalidException("Missing input input data.")

      result = user_service.create(input_data)
      response, status = r_helper.success_response(result, message="New user added.", status=201)

    except InputInvalidException as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def login(self) -> tuple[Response, int]:
    """Controller for root route."""
    try:
      input_data = request.json

      if input_data is None or "username" not in input_data:
        raise InputInvalidException("No username provided.")

      user = user_service.login(input_data["username"], "ps")
      response, status = r_helper.success_response(user, message="User logged in.", status=200)

    except (NoDataException, InputInvalidException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def single_user(self, id_num: int) -> tuple[Response, int]:
    """Controller for updating user.

    Parameters:
      id_num(int):  id for user

    Returns:
      response, status
    """
    try:
      if request.method == "PUT":
        input_data = request.json

        if input_data is None or "username" not in input_data:
          raise InputInvalidException("No username provided.")
        success = user_service.update(id_num, input_data)
        message = "User updated." if success else "User not updated."

        response, status = r_helper.success_response(message=message)
      else:
        data = user_service.get_by_id(id_num)
        response, status = r_helper.success_response(data)

    except (NoDataException, KeyUnmutableException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status