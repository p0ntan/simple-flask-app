"""
User model representing a user.
"""
from __future__ import annotations
from typing import Any
from src.static.types import UserData
from src.utils.daos.userdao import UserDAO
from src.errors.customerrors import NoDataException


class User():
  """User model representing a user."""
  def __init__(self, user_data: UserData):
    """Initiate the user.

    Args:
      user (UserData): Dictonary with needed data for user with keys:
        - user_id (int):
        - username (str):
        - role (str):
        - signature (str | None):
        - avatar (str | None):

    Raises:
      KeyError: In case of missing required keys
    """
    self._user_id = user_data["user_id"]
    self._username = user_data["username"]
    self._role = user_data["role"]
    self._signature = user_data.get("signature", None)
    self._avatar = user_data.get("avatar", None)

  @property
  def id(self) -> int:
    """Get the id of the user."""
    return self._user_id

  def update(self, user_data: dict[str, Any]):
    """Update the user with provided data.

    Args:
      user_data (dict): Dictionary with keys to update.
    
    Returns:
      new_data (dict):  Dict with only the updated data.
    """
    self._username = user_data.get("username", self._username)
    self._role = user_data.get("role", self._role)
    self._signature = user_data.get("signature", self._signature)
    self._avatar = user_data.get("avatar", self._avatar)

    return {
      "username": self._username,
      # "role": self._role,  TODO: Add add rights for only admin
      "signature": self._signature,
      "avatar": self._avatar
    }

  def to_dict(self) -> dict[str, Any]:
    """Return user data as dictionary.

    Returns:
      UserData: Dictionary with user data
    """
    result = {}

    for key, value in self.__dict__.items():
      key = key[1:] if key[0] == "_" else key
      result[key] = value.to_dict() if hasattr(value, 'to_dict') else value

    return result

  @classmethod
  def from_db_by_id(cls, user_id: int, user_dao: UserDAO) -> User:
    """Initiate user with data from database, by id.

    Args:
      user_id (int):      The id of the user.
      user_dao (UserDAO): An instance of the UserDAO class.

    Returns:
      User:               The user object.

    Raises:
      NoDataException:    If no user is found with given id.
    """
    user_data = user_dao.get_one(user_id)

    if user_data is None:
      raise NoDataException(f"No user found with id: {user_id}")

    return cls(user_data)
