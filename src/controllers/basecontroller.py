"""
Baseclass for all controllers.

They should all have create, get_one, update and delete methods.
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import Response, request, jsonify
from src.services.base_service import BaseService
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import InputInvalidException, NoDataException, KeyUnmutableException, UnauthorizedException

r_helper = ResponseHelper()


class Controller:
  """Base class for controllers."""

  def __init__(self, service: BaseService, controller_name: str):
    """Initializes the Controller class.

    Args:
      service (BaseService):  An instance of the BaseService class.
      controller_route (str): The route for the controller.
    """
    self._service = service
    self._controller = controller_name

  def create(self) -> tuple[Response, int]:
    """Controller for root route, creating a new entry.
  
    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      input_data = request.json

      if input_data is None:
        raise InputInvalidException("Missing input data.")

      result = self._service.create(input_data)  # TODO get id from token or other way
      response, status = r_helper.success_response(result, message=f"New {self._controller} added.", status=201)

    except (InputInvalidException, NoDataException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  def get_one(self, id_num: int) -> tuple[Response, int]:
    """Controller getting one entry from database.

    Args:
      id_num (int):         unique id for entry 

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

  @jwt_required()
  def update(self, id_num: int) -> tuple[Response, int]:
    """Controller for updating entry.

    Parameters:
      id_num(int):  id for entry

    Returns:
      tuple[Response, int]: The response and status code
    """
    try:
      input_data = request.json

      if input_data is None:
        raise InputInvalidException("Missing input data.")

      current_user = get_jwt_identity()
      success = self._service.update(id_num, input_data, current_user)
      message, status = (f"{self._controller} updated.", 200) if success else (f"{self._controller} not updated.", 202)

      response, status = r_helper.success_response(message=message, status=status)

    except (
      NoDataException,
      KeyUnmutableException,
      InputInvalidException,
      UnauthorizedException
    ) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status

  @jwt_required()
  def delete(self, id_num: int) -> tuple[Response, int]:
    """Controller for deleting entry.

    Parameters:
      id_num(int):  id for entry

    Returns:
      tuple[Response, int]: The response and status code
    """
    # TODO fix delete route
    try:
      current_user = get_jwt_identity()
      success = self._service.delete(id_num, current_user)

      message, status = (f"{self._controller} deleted.", 200) if success else (f"{self._controller} not deleted.", 202)

      response, status = r_helper.success_response(message=message, status=status)

    except (NoDataException, UnauthorizedException) as err:
      response, status = r_helper.error_response(err.status, details=f"{err}")
    except Exception as err:
      response, status = r_helper.unkown_error(details=f"{err}")

    return jsonify(response), status
