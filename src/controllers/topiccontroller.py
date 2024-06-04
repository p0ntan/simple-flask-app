"""
TopicController is for handling all calls to database regarding topics.
"""
from src.controllers.controller import Controller
from src.utils.dao import DAO
from src.utils.postdao import PostDAO


class TopicController(Controller):
  """ TopicController handles all dataaccess for topics. """
  def __init__(self, topic_dao: DAO, post_dao: PostDAO):
    super().__init__(dao=topic_dao)
    self._post_dao = post_dao

  def get_topic_and_posts(self, topic_id: int, pagnation: int = 0) -> list[dict]:
    """ Get posts for topic.

    Parameters:
      topic_id(int):  id for topic
      pagnation(int): for only getting 10 posts at time, 0 = first 10

    Returns:
      list[dict]:     list with posts
    """
    return self._post_dao.get_posts_and_topic(topic_id, pagnation)
