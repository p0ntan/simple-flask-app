"""
Usercontroller is for handling all calls to database regarding users.
"""
from flask import jsonify, request, Response
from src.controllers.basecontroller import Controller
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
    self._dao = user_dao

  def create(self) -> tuple[Response, int]:
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

  def get_one(self, id_num: int) -> tuple[Response, int]:
    """Controller for getting one user.

    Parameters:
      id_num(int):  id for user

    Returns:
      response, status
    """
    try:
      data = user_service.get_by_id(id_num)
      response, status = r_helper.success_response(data)

    except NoDataException as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def update(self, id_num: int) -> tuple[Response, int]:
    """Controller for updating user.

    Parameters:
      id_num(int):  id for user

    Returns:
      response, status
    """
    try:
      input_data = request.json

      if input_data is None or "username" not in input_data:
        raise InputInvalidException("No username provided.")
      success = user_service.update(id_num, input_data)
      message = "User updated." if success else "User not updated."

      response, status = r_helper.success_response(message=message)

    except (NoDataException, KeyUnmutableException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status
  
  def delete(self, id_num: int) -> tuple[Response, int]:
    """Controller for deleting user.

    Parameters:
      id_num(int):  id for user

    Returns:
      response, status
    """
    # TODO fix delete route
    try:
      success = user_service.delete(id_num)
      message = "User deleted." if success else "User not deleted."
      status = 200 if success else 202

      response, status = r_helper.success_response(message=message, status=status)

    except NoDataException as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status