"""
Usercontroller is for handling all calls to database regarding users.
"""
from flask import jsonify, request, Response
from src.controllers.basecontroller import Controller
from src.utils.response_helper import ResponseHelper
from src.services.user_service import UserService
from src.errors.customerrors import NoDataException, InputInvalidException
from flask_jwt_extended import create_access_token

r_helper = ResponseHelper()

class UserController(Controller):
  """ UserController handles all dataaccess for users. """
  def __init__(self, service: UserService, controller_name: str):
    """Initializes the UserController class.
    
    Args:
      service (UserService): An instance of the UserService class.
      controller_name (str): The name of the controller.

    Raises:
      InputInvalidException:  If input data is missing.
    """
    self._service = service
    self._controller = controller_name

  def login(self) -> tuple[Response, int]:
    """Controller for login route."""
    input_data = request.json

    if input_data is None:
      raise InputInvalidException("Missing input data.")

    user = self._service.login(input_data["username"], "ps")
    access_token = create_access_token(identity=user)

    response, status = r_helper.success_response({"jwt": access_token}, message="User logged in.", status=200)

    return jsonify(response), status
