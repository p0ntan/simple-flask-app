"""
DAO is used for simplyfying handling with data from database.
"""
import os
import sqlite3
from abc import ABC, abstractmethod
from typing import Any
from src.utils.print_colors import ColorPrinter

printer = ColorPrinter()


class DAO(ABC):
  """
  DAO is a class with some db-connecting methods and abstrac methods for CRUD.
  """

  def __init__(self, table_name: str):
    """Constructor for DAO."""
    self._db_path = os.environ.get(
      "SQLITE_PATH",
      "./db/db.sqlite"
    )
    self._table = table_name
    self._connection = None

  def _get_connection_and_cursor(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """ Connect to the sqlite database and get connection and cursor.

    Returns:
      connection, cursor: To use for executing queries
    """
    connection = sqlite3.connect(self._db_path)
    cursor = connection.cursor()

    return connection, cursor

  def _connect_get_cursor(self) -> sqlite3.Cursor:
    """ Connect to the sqlite database.

    Returns:
      sqlite3 cursor:
    """
    self._connection = sqlite3.connect(self._db_path)
    return self._connection.cursor()

  def _disconnect(self):
    """ Disconnects the connection. """
    if self._connection is not None:
      self._connection.close()

    self._connection = None

  @abstractmethod
  def create(self, data: dict) -> Any:
    pass

  @abstractmethod
  def get_one(self, id_num: int) -> Any:
    pass

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

      cur.execute(f"UPDATE {self._table} SET {columns} WHERE id = ?", (*data.values(), id_num, ))
      conn.commit()

      return cur.rowcount > 0
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()

  def delete(self, id_num: int) -> bool:
    """Delete entry from database (soft delete).

    Args:
      id_num (int): unique id for the entry to delete

    Returns:
      boolean:      True if item deleted, False otherwise

    Raises:
      Exception:    In case of any error
    """
    conn = None
    try:
      conn, cur = self._get_connection_and_cursor()
      cur.execute(f"UPDATE {self._table} SET deleted = CURRENT_TIMESTAMP WHERE id = ?", (id_num, ))
      conn.commit()

      return cur.rowcount > 0
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()
