"""
User model representing a user.
"""
from __future__ import annotations
from typing import Any
from src.static.types import UserData
from src.utils.daos.userdao import UserDAO
from src.errors.customerrors import NoDataException, UnauthorizedException


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

  def update(self, user_data: dict[str, Any], editor: User):
    """Update the user with provided data.

    Args:
      user_data (dict): Dictionary with keys to update.
    
    Returns:
      new_data (dict):  Dict with only the updated data.
    """
    self.control_access(editor)

    self._role = user_data.get("role", self._role)
    self._signature = user_data.get("signature", self._signature)
    self._avatar = user_data.get("avatar", self._avatar)

    return {
      # "role": self._role,  TODO: Add add rights for only admin
      "signature": self._signature,
      "avatar": self._avatar
    }

  def control_access(self, editor: User) -> None:
    """Control that another user (editor) can manage the user.

    Args:
      editor (User):          The user to control having access to manage this user.

    Raises:
      UnauthorizedException:  If the user (editor) is not authorized to manage the topic.
    """
    if editor.id != self.id:  # TODO add better logic, like admin/moderator.
      raise UnauthorizedException("User not authorized to manage this user.")

  def to_dict(self) -> UserData:
    """Return user data as dictionary.

    Returns:
      UserData: Dictionary with user data
    """
    result = {}

    for key, value in self.__dict__.items():
      key = key[1:] if key[0] == "_" else key
      result[key] = value.to_dict() if hasattr(value, 'to_dict') else value

    return UserData(**result)

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
