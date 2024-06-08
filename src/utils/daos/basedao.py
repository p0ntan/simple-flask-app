"""
DAO is used for simplyfying handling with data from database.
"""
import os
import sqlite3
from abc import ABC, abstractmethod
from typing import Any
from src.utils.print_colors import ColorPrinter
from src.errors.customerrors import KeyUnmutableException

printer = ColorPrinter()


class DAO(ABC):
  """
  DAO is for simpler access for tables in sqlite-db.
  """

  def __init__(self, table_name: str):
    """
    Parameters:
      table_name (str): tablename for the DAO.
    """
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

  @abstractmethod
  def update(self, id_num: int, data: dict) -> bool:
    pass

  # @abstractmethod
  # def delete(self, id_num: int) -> bool:
  #   pass