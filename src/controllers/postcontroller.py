"""
PostController is for handling all calls to database regarding posts.
"""
from flask import jsonify, request, Response
from src.controllers.basecontroller import Controller
from src.services import PostService
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import NoDataException, KeyUnmutableException, InputInvalidException

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
