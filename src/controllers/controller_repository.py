"""
Repository to handle controllers, using singleton princible.
"""
from src.utils.daos.dao import DAO
from src.utils.daos import PostDAO, TopicDAO, UserDAO
from src.controllers import UserController, TopicController, PostController
from src.services import UserService, TopicService


class ControllerRepository:
  """ A class for handling all controllers, having them easily accessed in rest of system. """
  _instance = None
  _controllers = {}

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(ControllerRepository, cls).__new__(cls)
    return cls._instance

  def get_user_controller(self) -> UserController:
    """ Get UserController. Creates an instance if not already in self._controllers.

    Returns:
      UserController: The UserController for data handling
    """
    if "user_controller" not in self._controllers:
      user_dao = UserDAO()
      user_service = UserService(user_dao)
      self._controllers["user_controller"] = UserController(user_service)
    return self._controllers["user_controller"]

  def get_topic_controller(self) -> TopicController:
    """ Get TopicController. Creates an instance if not already in self._controllers.

    Returns:
      TopicController: The TopicController for data handling
    """
    if "topic_controller" not in self._controllers:
      topic_dao = TopicDAO()
      user_dao = UserDAO()
      post_dao = PostDAO("post")
      topic_service = TopicService(topic_dao, user_dao, post_dao)
      self._controllers["topic_controller"] = TopicController(topic_service)
    return self._controllers["topic_controller"]

  def get_post_controller(self) -> PostController:
    """ Get PostController. Creates an instance if not already in self._controllers.

    Returns:
      PostController: The PostController for data handling
    """
    if "post_controller" not in self._controllers:
      post_dao = DAO(table_name="post")
      self._controllers["post_controller"] = PostController(post_dao)
    return self._controllers["post_controller"]
