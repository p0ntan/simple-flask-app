from src.controllers.controller import Controller
from src.utils.dao import DAO


class TopicController(Controller):
  def __init__(self, topic_dao: DAO):
    super().__init__(dao=topic_dao)
