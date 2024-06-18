"""
Usercontroller is for handling all calls to database regarding users.
"""

from flask import jsonify, request, Response
from src.controllers.basecontroller import Controller
from src.utils.response_helper import ResponseHelper
from src.services.user_service import UserService
from src.errors.customerrors import InputInvalidException
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

r_helper = ResponseHelper()


class UserController(Controller):
    """UserController handles all dataaccess for users."""

    def __init__(self, service: UserService, controller_name: str):
        """Initializes the UserController class.

        Args:
          service (UserService): An instance of the UserService class.
          controller_name (str): The name of the controller.

        Returns:
          tuple[Response, int]: The response and status code

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

        response, status = r_helper.success_response(
            {"user": user, "jwt": access_token}, message="User logged in.", status=200
        )

        return jsonify(response), status

    @jwt_required()
    def upload_image(self, id_num: int) -> tuple[Response, int]:
        """Controller for route where user can upload an avatar image.

        Args:
          id_num (int): Id number for the user to upload image for.

        Returns:
          tuple[Response, int]: The response and status code

        Raises:
          InputInvalidException:  If input data is missing.
        """
        if "file" not in request.files:
            raise InputInvalidException("Missing image file.")

        file = request.files["file"]

        if file.filename == "" or not file:
            raise InputInvalidException("Missing image file.")

        current_user = get_jwt_identity()
        success = self._service.upload_avatar(id_num, file, current_user)

        if success:
            message, status = "Image uploaded and updated", 200
        else:
            message, status = "Image not uploaded or updated.", 202

        response, status = r_helper.success_response(message=message, status=status)
        return jsonify(response), status
