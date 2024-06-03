"""
PostController is for handling all calls to database regarding posts.
"""
from src.controllers.controller import Controller
from src.utils.dao import DAO


class PostController(Controller):
  """ PostController handles all dataaccess for posts. """
  def __init__(self, post_dao: DAO):
    super().__init__(dao=post_dao)
