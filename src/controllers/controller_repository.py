"""
Repository to handle controllers, using singleton princible.
"""
from src.utils.daos.dao import DAO
from src.utils.daos.postdao import PostDAO
from src.utils.daos.userdao import UserDAO
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

  def get_user_controller(self) -> UserController:
    """ Get UserController. Creates an instance if not already in self._controllers.

    Returns:
      UserController: The UserController for data handling
    """
    if "user_controller" not in self._controllers:
      user_dao = UserDAO(table_name="user")
      self._controllers["user_controller"] = UserController(user_dao)
    return self._controllers["user_controller"]

  def get_topic_controller(self) -> TopicController:
    """ Get TopicController. Creates an instance if not already in self._controllers.

    Returns:
      TopicController: The TopicController for data handling
    """
    if "topic_controller" not in self._controllers:
      topic_dao = DAO(table_name="topic")
      post_dao = PostDAO(table_name="post")
      self._controllers["topic_controller"] = TopicController(topic_dao, post_dao)
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
