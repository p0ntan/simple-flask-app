"""
Repository to handle controllers, using singleton princible.
"""
from src.utils.dao import DAO
from src.controllers.controller import Controller
from src.controllers.usercontroller import UserController
from src.controllers.topiccontroller import TopicController
from src.controllers.postcontroller import PostController


class ControllerRepository:
  """ A class for handling all controllers, having them easily accessed in rest of system. """
  _instance = None
  _controllers = {}

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(ControllerRepository, cls).__new__(cls)
    return cls._instance

  def get_user_controller(self) -> Controller:
    """ Get UserController. Creates an instance if not already in self._controllers.

    Returns:
      Controller:   The UserController for data handling
    """
    if "user_controller" not in self._controllers:
      user_dao = DAO(table_name="user")
      self._controllers["user_controller"] = UserController(user_dao)
    return self._controllers["user_controller"]

  def get_topic_controller(self) -> Controller:
    """ Get TopicController. Creates an instance if not already in self._controllers.

    Returns:
      Controller:   The TopicController for data handling
    """
    if "topic_controller" not in self._controllers:
      topic_dao = DAO(table_name="topic")
      self._controllers["topic_controller"] = TopicController(topic_dao)
    return self._controllers["topic_controller"]

  def get_post_controller(self) -> Controller:
    """ Get PostController. Creates an instance if not already in self._controllers.

    Returns:
      Controller:   The PostController for data handling
    """
    if "post_controller" not in self._controllers:
      post_dao = DAO(table_name="post")
      self._controllers["post_controller"] = PostController(post_dao)
    return self._controllers["post_controller"]
