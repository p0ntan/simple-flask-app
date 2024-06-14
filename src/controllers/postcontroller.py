"""
PostController is for handling all calls to database regarding posts.
"""

from flask import jsonify, request, Response
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.controllers.basecontroller import Controller
from src.services import PostService
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import InputInvalidException

r_helper = ResponseHelper()


class PostController(Controller):
    """PostController handles all dataaccess for posts."""

    def __init__(self, service: PostService, controller_name: str):
        """Initializes the PostController class.

        Args:
          service (PostService): An instance of the PostService class.
          controller_name (str): The name of the controller.
        """
        super().__init__(service, controller_name)

    @jwt_required()
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

        current_user = get_jwt_identity()
        result = self._service.create(input_data, current_user)
        response, status = r_helper.success_response(
            result, message=f"New {self._controller} added.", status=201
        )

        return jsonify(response), status
