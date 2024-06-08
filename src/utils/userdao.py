"""
UserDAO is used for accessing users.
"""
from __future__ import annotations
from src.models.user import User
from src.utils.dao import DAO
from src.utils.print_colors import ColorPrinter

printer = ColorPrinter()


class UserDAO(DAO):
  """ UserDAO for accessing posts. """

  def __init__(self, table_name: str):
    super().__init__(table_name=table_name)

  def create(self, data: dict[str, str]) -> dict[str, int | str | None]:
    """ Create (insert) a new entry into database.

    Returns:
      dict:         with new entry

    Raises:
      Exception:    in case of any error like invalid input keyp or unique entry already exist.
    """
    conn = None

    try:
      conn, cur = self._get_connection_and_cursor()
      cur.execute(f"INSERT INTO user (username) VALUES (?)", (data["username"], ))

      conn.commit()

      return {"id": cur.lastrowid, **data}
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()

  def get_user_by_username(self, username: str) -> User | None:
    """Retrieves a user from the database by their username.

    Args:
      username (str): The username of the user to retrieve.

    Returns:
      User: The user object if found
      None: None if not found.

    Raises:
      Exception: If an error occurs while retrieving the user.
    """
    try:
      cur = self._connect_get_cursor()

      cur.execute("SELECT * FROM user WHERE username = ?", (username, ))
      column_names = [description[0] for description in cur.description]
      result = cur.fetchone()

      if result is None:
        return result

      user_data = dict(zip(column_names, result))
      user_id: int = user_data.pop("id")

      return User(user_id, user_data)  # type: ignore
    except Exception as error:
      printer.print_fail(error)
      raise error
    finally:
      self._disconnect()
