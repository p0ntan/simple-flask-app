"""
UserDAO is used for accessing users.
"""
from __future__ import annotations
from typing import Any
from src.models.user import User, UserData
from src.utils.daos.basedao import DAO
from src.utils.print_colors import ColorPrinter

printer = ColorPrinter()


class UserDAO(DAO):
  """ UserDAO for accessing posts. """
  GET_ONE_QUERY_USERNAME = "SELECT id AS user_id, username, role, signature, avatar FROM user WHERE username = ?"
  GET_ONE_QUERY_ID = "SELECT id as user_id, username, role, signature, avatar FROM user WHERE id = ?"

  def __init__(self, table_name: str):
    super().__init__(table_name=table_name)

  def create(self, data: dict[str, str]) -> UserData:
    """Create (insert) a new entry into database.

    Parameters:
      data (dict):  The data for the new user.

    Returns:
      UserData:     Dictonary with the new user.

    Raises:
      Exception:    in case of any error like unique entry already exist.
    """
    conn = None

    try:
      conn, cur = self._get_connection_and_cursor()
      cur.execute(f"INSERT INTO user (username) VALUES (?)", (data["username"], ))
      conn.commit()

      cur.execute(self.GET_ONE_QUERY_ID, (cur.lastrowid, ))
      column_names = [description[0] for description in cur.description]
      result = cur.fetchone()

      user_data = dict(zip(column_names, result))

      return UserData(**user_data)
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()

  # TODO make this method better
  def update(self, id_num: int, data: dict) -> bool:
    """Update entry.

    Parameters:
      id_num (int): unique id for the entry to update
      data (dict):  dictionary with new data

    Returns:
      boolean:      True if item changed, False otherwise

    Raises:
      Exception:    In case of any error
    """
    conn = None
    try:
      conn, cur = self._get_connection_and_cursor()

      columns = ', '.join([f'{k} = ?' for k in data.keys()])

      cur.execute(f"UPDATE user SET {columns} WHERE id = ?", (*data.values(), id_num, ))
      conn.commit()

      return cur.rowcount > 0
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()

  def get_user_by_username(self, username: str) -> UserData | None:
    """Retrieves a user from the database by their username.

    Parameters:
      username (str): The username of the user to retrieve.

    Returns:
      UserData:       Dictonary with the user.
      None:           None if not found.

    Raises:
      Exception:      If an error occurs while retrieving the user.
    """
    try:
      cur = self._connect_get_cursor()

      cur.execute(self.GET_ONE_QUERY_USERNAME, (username, ))
      column_names = [description[0] for description in cur.description]
      result = cur.fetchone()

      if result is None:
        return result

      user_data = dict(zip(column_names, result))

      return UserData(**user_data)
    except Exception as error:
      printer.print_fail(error)
      raise error
    finally:
      self._disconnect()

  def get_one(self, id_num: int) -> UserData | None:
    """Retrieves a user from the database by their id.

    Parameters:
      id_num (int): The id of the user to retrieve.

    Returns:
      UserData:     Dictonary with the user.
      None:         None if not found.

    Raises:
      Exception:    If an error occurs while retrieving the user.
    """
    try:
      cur = self._connect_get_cursor()

      cur.execute(self.GET_ONE_QUERY_ID, (id_num, ))
      column_names = [description[0] for description in cur.description]
      result = cur.fetchone()

      if result is None:
        return result

      user_data = dict(zip(column_names, result))

      return UserData(**user_data)
    except Exception as error:
      printer.print_fail(error)
      raise error
    finally:
      self._disconnect()
