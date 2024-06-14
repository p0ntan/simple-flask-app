"""
Post model representing a post.
"""
from __future__ import annotations
from typing import Any
from src.static.types import PostData
from src.models.user import User
from src.errors.customerrors import UnauthorizedException, NoDataException
from src.utils.daos import PostDAO


class Post():
  """Post model representing a post."""
  def __init__(self, author: User, post_data: PostData):
    """Initiate a post.

    Parameters:
      author (User):          User who created the post
      post_data (PostData):   Dictonary with needed data for post with keys
        - post_id (int):                id for post
        - topic_id (int):               id for topic
        - title (str):                  title for post
        - body                          body for post
        - created (str):                timestamp when post was created
        - last_edited (str | None):     timestamp when post was last edited
        - deleted (str | None):         timestamp when post was deleted (softly)
        - disabled (bool):              boolean if post is disabled

    Raises:
      KeyError: In case of missing required keys
    """
    self._author = author
    self._post_id = post_data["post_id"]
    self._topic_id = post_data["topic_id"]
    self._title = post_data.get("title", None)
    self._body = post_data["body"]
    self._created = post_data["created"]
    self._last_edited = post_data.get("last_edited", None)
    self._deleted = post_data.get("deleted", None)

  def update(self, post_data: dict[str, Any], editor: User) -> dict[str, Any]:
    """Update the post with provided data.

    Args:
      post_data (dict):   Dictionary with keys to update.
      editor (User):      The user who is wanting to update the post.

    Returns:
      new_data (dict):    Dict with only the updated data.

    Raises:
      UnauthorizedException: If the user is not authorized to manage the post.
    """
    if not self.editor_has_permission(editor):
      raise UnauthorizedException("User not authorized to manage post.")

    # TODO update logic below. As of now it returns all updatedable keys even if not provided by editor.
    # However, if no valid updateable keys are given it would result in a db-error when trying to update.
    # Same with user and topic.
    self._title = post_data.get("title", self._title)
    self._body = post_data.get("body", self._body)

    return {"title": self._title, "body": self._body}
  
  def editor_has_permission(self, editor: User) -> bool:
    """Control that another user (editor) can manage the post based on id and access.

    Args:
      editor (User):          The editor to control having access to manage this post.

    Returns:
      has_permission (bool):  True if edditor has permission, False if not.
    """
    # TODO add more (better) logic when time comes, like admin/moderator.
    return editor.id == self._author.id

  def to_dict(self) -> PostData:
    """Return post data as dictionary.

    Returns:
      (dict): Dictionary with post data
    """
    result = {}

    for key, value in self.__dict__.items():
      key = key[1:] if key[0] == "_" else key
      result[key] = value.to_dict() if hasattr(value, 'to_dict') else value

    return PostData(**result)

  @classmethod
  def from_db_by_id(cls, post_id: int, post_dao: PostDAO) -> Post:
    """Initiate post with data from database, by id.

    Parameters:
      post_id (int):      The id of the post.
      post_dao (PostDAO): An instance of the PostDAO class.

    Returns:
      Post:               The post object.

    Raises:
      NoDataException:      If no post is found with given id.
    """
    post_data = post_dao.get_one(post_id)

    if post_data is None:
      raise NoDataException(f"No topic found with id: {post_id}")
    
    user_data = post_data.pop("author")

    return cls(User(user_data), post_data)