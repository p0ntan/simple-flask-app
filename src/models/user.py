"""
User model representing a user.
"""
from typing import TypedDict, NotRequired

class UserData(TypedDict):
  id: int
  username: str
  role: str
  signature: NotRequired[str]
  avatar: NotRequired[str]

class UserUpdateData(UserData, total=False):
  """User model representing a user when updating data."""

class User():
  """User model representing a user."""

  def __init__(self, user_data: UserData):
    """Initiate the user.
    
    Parameters:
      user (UserData): Dictonary with needed data for user with keys:
        - id (int):
        - username (str):
        - role (str):
        - signature (NotRequired[str])
        - avatar (NotRequired[str])
    """
    self.id = user_data['id']
    self.username = user_data['username']
    self.role = user_data['role']
    self.signature = user_data.get('signature', None)
    self.avatar = user_data.get('avatar', None)

  def update(self, user_data: UserUpdateData):
    """Update the user with provided data.
    
    Parameters:
      user_data (UserUpdateData): Dictionary with keys to update.
    """
    self._id = user_data.get('id', self._id)
    self._username = user_data.get('username', self._username)
    self._role = user_data.get('role', self._role)
    self._signature = user_data.get('signature', self._signature)
    self._avatar = user_data.get('avatar', self._avatar)

  def to_dict(self) -> UserData:
    """Return user data as dictionary.
    
    Returns:
      UserData (dict): Dictionary with user data
    """
    return {
      'id': self._id,
      'username': self._username,
      'role': self._role,
      'signature': self._signature,
      'avatar': self._avatar
    }
