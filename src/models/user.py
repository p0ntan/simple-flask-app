"""
User model representing a user.
"""
from __future__ import annotations
from typing import TypedDict


class UserInput(TypedDict):
  """UserInput representing input data when creating a User."""
  username: str
  role: str
  signature: str | None
  avatar: str | None


class UserData(UserInput):
  """UserData representing user data."""
  user_id: int


class User():
  """User model representing a user."""
  def __init__(self, user_data: UserData):
    """Initiate the user.

    Parameters:
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

  def update(self, user_data: UserInput):
    """Update the user with provided data.

    Parameters:
      user_data (UserInput): Dictionary with keys to update.
    """
    self._username = user_data.get('username', self._username)
    self._role = user_data.get('role', self._role)
    self._signature = user_data.get('signature', self._signature)
    self._avatar = user_data.get('avatar', self._avatar)

  def to_dict(self) -> UserData:
    """Return user data as dictionary.

    Returns:
      UserData: Dictionary with user data
    """
    return {
      'user_id': self._user_id,
      'username': self._username,
      'role': self._role,
      'signature': self._signature,
      'avatar': self._avatar
    }
