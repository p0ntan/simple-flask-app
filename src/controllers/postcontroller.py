from src.controllers.controller import Controller
from src.utils.dao import DAO


class PostController(Controller):
  def __init__(self, post_dao: DAO):
    super().__init__(dao=post_dao)
