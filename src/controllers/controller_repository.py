"""
Repository to handle controllers, using singleton princible.
"""
from src.utils.dao import DAO
from src.controllers.controller import Controller
from src.controllers.usercontroller import UserController

class ControllerRepository:
  _instance = None
  _controllers = {}

  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(ControllerRepository, cls).__new__(cls)
      print("inne och skapar")
    return cls.instance

  def get_user_controller(self) -> Controller:
    """ Get UserController. Creates an instance if not already in self._controllers.

    Returns:
      Controller:   The UserController for data handling
    """
    if "user_controller" not in self._controllers:
      user_dao = DAO(table_name="user")
      self._controllers["user_controller"] = UserController(user_dao)
    return self._controllers["user_controller"]
