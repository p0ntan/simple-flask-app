"""
Baseclass for all controllers.

They should all have create, get_one, update and delete methods which can be overrun in the inheriting classes.
All errors raised here or in the inheriting classes or in any of the classes used in the controllers will be
handled at a higher level (the apiblueprint).
"""

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import Response, request, jsonify
from src.services.base_service import BaseService
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import InputInvalidException

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
          tuple[Response, int]:   The response and status code

        Raises:
          InputInvalidException:  If input data is missing.
        """
        input_data = request.json

        if input_data is None:
            raise InputInvalidException("Missing input data.")

        result = self._service.create(input_data)
        response, status = r_helper.success_response(
            result, message=f"New {self._controller} added.", status=201
        )

        return jsonify(response), status

    def get_one(self, id_num: int) -> tuple[Response, int]:
        """Controller getting one entry from database.

        Args:
          id_num (int):         unique id for entry

        Returns:
          tuple[Response, int]: The response and status code
        """
        result = self._service.get_by_id(id_num)
        response, status = r_helper.success_response(result)

        return jsonify(response), status

    @jwt_required()
    def update(self, id_num: int) -> tuple[Response, int]:
        """Controller for updating entry. Getting new data from request body.

        Args:
          id_num(int):  id for entry

        Returns:
          tuple[Response, int]: The response and status code

        Raises:
          InputInvalidException:  If input data is missing.
        """
        input_data = request.json

        if input_data is None:
            raise InputInvalidException("Missing input data.")

        current_user = get_jwt_identity()
        success = self._service.update(id_num, input_data, current_user)
        message, status = (
            (f"{self._controller} updated.", 200)
            if success
            else (f"{self._controller} not updated.", 202)
        )

        response, status = r_helper.success_response(message=message, status=status)

        return jsonify(response), status

    @jwt_required()
    def delete(self, id_num: int) -> tuple[Response, int]:
        """Controller for deleting entry.

        Args:
          id_num(int):  id for entry

        Returns:
          tuple[Response, int]: The response and status code
        """
        current_user = get_jwt_identity()
        success = self._service.delete(id_num, current_user)

        message, status = (
            (f"{self._controller} deleted.", 200)
            if success
            else (f"{self._controller} not deleted.", 202)
        )
        response, status = r_helper.success_response(message=message, status=status)

        return jsonify(response), status
