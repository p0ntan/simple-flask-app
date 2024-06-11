"""
Module for user service, main purpose to handle users in the application.

This will be used by controllers to keep the logic here and not in controller.
"""
from src.utils.daos.userdao import UserDAO
from src.models.user import UserData
from src.errors.customerrors import NoDataException


class UserService:
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

  def update(self, id_num: int, data: dict[str, str]) -> bool:
    """Update a user in the database.

    Parameters:
      id_num (int): The id of the user.
      data (dict):  New data.

    Returns:
      Boolean: True if item changed, False otherwise
    """
    user = self._dao.update(id_num, data)
    return user

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
    """Update a user in the database.

    Parameters:
      data (dict): New data.

    Returns:
      UserData: The user as a dictionary.
  
    Raises:
      NoDataException: If no user is found with the given username.
    """
    user = self._dao.get_one(user_id)

    if user is None:
      raise NoDataException(f"No user found with user_id: {user_id}")
    
    return user
