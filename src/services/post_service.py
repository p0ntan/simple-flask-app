"""
Module for post service, main purpose to handle posts in the application.

This will be used by controllers to keep the logic here and not in controller.
"""
from typing import Any
from src.services.base_service import BaseService
from src.models import Post, User
from src.utils.daos import PostDAO, UserDAO
from src.static.types import PostData, UserData
from src.errors.customerrors import NoDataException, UnauthorizedException


class PostService(BaseService):
  """
  PostService is used for post handling.
  """
  def __init__(self, dao: PostDAO, user_dao: UserDAO):
    """Initializes the PostService class.

    Args:
      dao (PostDAO): An instance of the PostDAO class.
    """
    self._dao = dao
    self._user_dao = user_dao

  def create(self, data: dict[str, Any], creator: UserData) -> PostData:
    """Creates a new post in the database.

    Args:
      data (dict):  The data for the new post.

    Returns:
      PostData:     The post as a dictionary if created successfully.
    """
    user = User(creator)
    data["author"] = user.id
    # TODO add logic for user control here by calling method on User ex. user.can_create_post()
    # and maybe raise exception if not allowed, might be the cleanest solution.
    # if not user.can_create_post():
    #     raise Exception("User is not allowed to create topic")
    return self._dao.create(data)

  def update(self, post_id: int, new_data: dict[str, Any], editor_data: UserData) -> bool:
    """Update a topic in the database.

    Args:
      post_id (int):          The id of the topic.
      new_data (dict):        New data.
      editor_data (UserData): The data of the editor trying to update topic.

    Returns:
      Boolean:                True if topic changed, False otherwise
    """
    editor = User(editor_data)
    post = Post.from_db_by_id(post_id, post_dao=self._dao)

    data_to_db = post.update(new_data, editor)
    result = self._dao.update(post_id, data_to_db)  # TODO returns true if nothing has changed but user is found

    return result

  def delete(self, id_num: int, editor_data: UserData) -> bool:
    """Delete a user in the database.

    Args:
      id_num (int):           The id of the user.
      editor_data (UserData): The data of the editor trying to delete topic.

    Returns:
      Boolean:                True if item deleted, False otherwise
  
    Raises:
      UnauthorizedException: If the user is not authorized to manage the topic.
    """
    editor = User(editor_data)
    post = Post.from_db_by_id(id_num, post_dao=self._dao)

    if not post.editor_has_permission(editor):
      raise UnauthorizedException("User not authorized to delete post.")

    success = self._dao.delete(id_num)
    return success

  def get_by_id(self, post_id: int) -> PostData:
    """Get a post from the database.

    Args:
      post_id (int):  The id of the post.

    Returns:
      PostData:       The post as a dictionary.
  
    Raises:
      NoDataException: If no user is found with the given username.
    """
    post_data = self._dao.get_one(post_id)

    if post_data is None:
      raise NoDataException(f"No post found with post_id: {post_id}")

    return post_data
