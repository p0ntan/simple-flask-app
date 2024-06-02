from src.controllers.controller import Controller
from src.utils.dao import DAO

class UserController(Controller):
  def __init__(self, user_dao: DAO):
    super().__init__(dao=user_dao)
