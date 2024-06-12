"""
Usercontroller is for handling all calls to database regarding users.
"""
from flask import jsonify, request, Response
from src.controllers.basecontroller import Controller
from src.utils.response_helper import ResponseHelper
from src.services.user_service import UserService
from src.errors.customerrors import NoDataException, InputInvalidException, KeyUnmutableException

r_helper = ResponseHelper()

class UserController(Controller):
  """ UserController handles all dataaccess for users. """
  def __init__(self, service: UserService, controller_name: str):
    """Initializes the UserController class.
    
    Args:
      service (UserService): An instance of the UserService class.
      controller_name (str): The name of the controller.
    """
    self._service = service
    self._controller = controller_name

  def login(self) -> tuple[Response, int]:
    """Controller for root route."""
    try:
      input_data = request.json

      if input_data is None or "username" not in input_data:
        raise InputInvalidException("No username provided.")

      user = self._service.login(input_data["username"], "ps")
      response, status = r_helper.success_response(user, message="User logged in.", status=200)

    except (NoDataException, InputInvalidException) as err:
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
      success = self._service.delete(id_num)
      message, status = ("User deleted.", 200) if success else ("User not deleted.", 202)

      response, status = r_helper.success_response(message=message, status=status)

    except NoDataException as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status