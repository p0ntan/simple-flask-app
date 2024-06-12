"""
Module for topic service, main purpose to handle topics in the application.

This will be used by controllers to keep the logic here and not in controller.
"""
from typing import Any
from src.services.base_service import BaseService
from src.errors.customerrors import NoDataException
from src.models.user import User
from src.models.topic import Topic, TopicData
from src.utils.daos import TopicDAO, PostDAO, UserDAO
from src.static.types import TopicData, UserData


class TopicService(BaseService):
  """
  TopicService is for handling all calls to models and database regarding topics.
  """

  def __init__(self, topic_dao: TopicDAO, user_dao: UserDAO, post_dao: PostDAO) -> None:
    """
    Initializes the TopicService class.

    Args:
      topic_dao (TopicDAO): An instance of the TopicDAO class.
      user_dao (UserDAO):   An instance of the UserDAO class.
      post_dao (PostDAO):   An instance of the PostDAO class.
    """
    self._topic_dao = topic_dao
    self._user_dao = user_dao
    self._post_dao = post_dao

  def create(self, topic_data: dict[str, Any]) -> TopicData:
    """Creates a new topic.

    Args:
      topic_data (dict):  The data for the new topic.

    Returns:
      TopicData (dict):   The topic as a dictionary if created successfully.
    
    Raises:
      NoDataException:    If no user is found with the given id to create the topic.
    """
    # TODO remember to change way to get id of editor.
    user_id = topic_data["created_by"]
    user_data = self._user_dao.get_one(user_id)

    if user_data is None:
      raise NoDataException(f"No user found with id: {user_id}")

    user = User(user_data)
    # TODO add logic for user control here by calling method on User ex. user.can_create_topic()
    # and maybe raise exception if not allowed, might be the cleanest solution.
    # if not user.can_create_topic():
    #     raise Exception("User is not allowed to create topic")
    new_topic_data = self._topic_dao.create(topic_data)
    topic = Topic(user, new_topic_data)

    return topic.to_dict()

  def get_by_id(self, topic_id: int) -> TopicData:
    """Get one topic in the database.

    Args:
      topic_id (int):   The id of the topic.

    Returns:
      TopicData (dict): The topic as a dictionary, including user.
  
    Raises:
      NoDataException:  If no user is found with the given username.
    """
    topic_data = self._topic_dao.get_one(topic_id)

    if topic_data is None:
      raise NoDataException(f"No topic found with topic_id: {topic_id}")

    return topic_data

  def update(self, topic_id: int, new_data: dict[str, Any], editor_data: UserData) -> bool:
    """Update a topic in the database.

    Args:
      topic_id (int):         The id of the topic.
      new_data (dict):        New data.
      editor_data (UserData): The data of the editor trying to update topic.

    Returns:
      Boolean:                True if topic changed, False otherwise
    """
    editor = User(editor_data)
    topic = Topic.from_db_by_id(topic_id, topic_dao=self._topic_dao)

    data_to_db = topic.update(new_data, editor)
    result = self._topic_dao.update(topic_id, data_to_db)  # TODO returns true if nothing has changed but user is found

    return result

  def get_topic_posts_users(self, topic_id: int, pagnation: int = 0) -> dict[str, Any]:
    """Get topic and posts for topic.
    
    Args:
      topic_id (int):     The id of the topic.
      pagnation (int):    The number of pages to get.

    Returns:
      topic_data (dict):  The topic and posts as a dictionary.

    Raises:
      NoDataException:    If no topic is found with the given username.
    """
    topic_data = self.get_by_id(topic_id)
    posts_data = self._post_dao.get_post_and_users_with_pagination(topic_id, pagnation)

    return {
      "topic": topic_data,
      "posts": posts_data
    }

  def delete(self, topic_id: int, editor_data: UserData) -> bool:
    """Delete a topic in the database, (soft delete).
    Controls that the user trying to change the topic is allowed to do so.

    Args:
      topic_id (int):         The id of the topic.
      editor_data (UserData): The data of the editor trying to delete topic.

    Returns:
      Boolean:                True if item deleted, False otherwise
    """
    editor = User(editor_data)
    topic = Topic.from_db_by_id(topic_id, topic_dao=self._topic_dao)

    topic.control_access(editor)
    success = self._topic_dao.delete(topic_id)

    return success
