"""
Module for user service, main purpose to handle users in the application.

This will be used by controllers to keep the logic here and not in controller.
"""
from src.utils.userdao import UserDAO
from src.models.user import UserReturnData
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

  def create(self, data: dict) -> dict[str, str | int | None]:
    """Creates a new user in the database.

    Parameters:
      data (dict): The data for the new user.

    Returns:
      UserReturnData: The user as a dictionary if created successfully.
    """
    user = self._dao.create(data)
    return user

  def login(self, username: str, password: str) -> UserReturnData:
    """Login method for user

    Parameters:
      username (str): The username of the user.
      password (str): The password of the user.

    Returns:
      UserReturnData: The user as a dictionary if found.
    
    Raises:
      NoDataException: If no user is found with the given username.
    """
    password = password  # TODO add logic for password handling
    user = self._dao.get_user_by_username(username)

    if user is None:
      raise NoDataException(f"No user found with username: {username}")

    return user.to_dict()
