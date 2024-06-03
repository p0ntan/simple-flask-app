"""
TopicController is for handling all calls to database regarding topics.
"""
from src.controllers.controller import Controller
from src.utils.dao import DAO


class TopicController(Controller):
  """ TopicController handles all dataaccess for topics. """
  def __init__(self, topic_dao: DAO):
    super().__init__(dao=topic_dao)
