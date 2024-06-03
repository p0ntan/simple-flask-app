"""
Usercontroller is for handling all calls to database regarding users.
"""
from src.controllers.controller import Controller
from src.utils.dao import DAO


class UserController(Controller):
  """ UserController handles all dataaccess for users. """
  def __init__(self, user_dao: DAO):
    super().__init__(dao=user_dao)
