"""
Module for user service, main purpose to handle users in the application.

This will be used by controllers to keep the logic here and not in controller.
"""
from typing import Any
from src.services.base_service import BaseService
from src.utils.daos.userdao import UserDAO
from src.models import User
from src.static.types import UserData
from src.errors.customerrors import NoDataException


class UserService(BaseService):
  """
  UserService is used for user handling.
  """
  def __init__(self, dao: UserDAO):
    """Initializes the UserService class.

    Parameters:
      dao (UserDAO): An instance of the UserDAO class.
    """
    self._dao = dao

  def create(self, data: dict[str, str]) -> UserData:
    """Creates a new user in the database.

    Parameters:
      data (dict): The data for the new user.

    Returns:
      UserReturnData: The user as a dictionary if created successfully.
    """
    return self._dao.create(data)

  def update(self, user_id: int, new_data: dict[str, Any]) -> bool:
    """Update a user in the database.

    Args:
      user_id (int):    The id of the user.
      new_data (dict):  New data.

    Returns:
      Boolean:          True if topic changed, False otherwise
    """
    # TODO remember to change way to get id of editor
    user = User.from_db_by_id(user_id, self._dao)

    data_to_db = user.update(new_data)
    result = self._dao.update(user_id, data_to_db)  # TODO returns true if nothing has changed but user is found

    return result

  def delete(self, id_num: int) -> bool:
    """Delete a user in the database.

    Parameters:
      id_num (int): The id of the user.

    Returns:
      Boolean: True if item deleted, False otherwise
    """
    # user = self._dao.delete(id_num)
    # TODO implement soft delete
    return False

  def login(self, username: str, password: str) -> UserData:
    """Login and get data for a user.

    Parameters:
      username (str): The username of the user.
      password (str): The password of the user.

    Returns:
      UserData: The user as a dictionary

    Raises:
      NoDataException: If no user is found with the given username.
    """
    password = password  # TODO add logic for password handling
    user = self._dao.get_user_by_username(username)

    if user is None:
      raise NoDataException(f"No user found with username: {username}")

    return user

  def get_by_id(self, user_id: int) -> UserData:
    """Get a user in the database.

    Parameters:
      user_id (int):  The id of the user.

    Returns:
      UserData:       The user as a dictionary.
  
    Raises:
      NoDataException: If no user is found with the given username.
    """
    user = self._dao.get_one(user_id)

    if user is None:
      raise NoDataException(f"No user found with user_id: {user_id}")
    
    return user
