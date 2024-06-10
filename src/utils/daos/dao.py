"""
DAO is used for simplyfying handling with data from database.
"""
import os
import sqlite3
from src.utils.print_colors import ColorPrinter
from src.errors.customerrors import KeyUnmutableException

printer = ColorPrinter()


class DAO:
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

  def get_all(self) -> list[dict]:
    """ Get all data from table.

    Returns:
      list[dict]:   A list with dictionaries with all data

    Raises:
      Exception:    in case of any error
    """
    try:
      cur = self._connect_get_cursor()

      rows = cur.execute(f"SELECT * FROM {self._table}")
      column_names = [description[0] for description in cur.description]

      result = [dict(zip(column_names, row)) for row in rows]

      return result
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      self._disconnect()

  def get_one(self, id_num: int) -> dict:
    """ Get one entry

    Parameters:
      id_num (int): the unique id for the entry in database

    Returns:
      dict:         with data from single entry
      None:         if no entry found with given id

    Raises:
      Exception:    in case of any error
    """
    try:
      cur = self._connect_get_cursor()

      cur.execute(f"SELECT * FROM {self._table} WHERE id = ?", (id_num, ))
      column_names = [description[0] for description in cur.description]

      result = cur.fetchone()

      if result is not None:
        result = dict(zip(column_names, result))

      return result
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      self._disconnect()

  def create(self, data: dict) -> dict:
    """ Create (insert) a new entry into database.

    Returns:
      dict:         with new entry

    Raises:
      Exception:    in case of any error like invalid input keyp or unique entry already exist.
    """
    try:
      self._control_keys(data.keys())

      cur = self._connect_get_cursor()

      columns = ','.join(data.keys())
      placeholders = ",".join("?" * len(data.keys()))

      cur.execute(f"INSERT INTO {self._table} ({columns}) VALUES ({placeholders})", (*data.values(), ))

      self._connection.commit()

      return {"id": cur.lastrowid, **data}
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      self._disconnect()

  def update(self, id_num: int, data: dict) -> bool:
    """ Update entry.

    Parameters:
      id_num (int): unique id for the entry to update
      data (dict):  dictionary with new data

    Returns:
      boolean:      True if item changed, False otherwise

    Raises:
      Exception:    In case of any error
    """
    try:
      self._control_keys(data.keys())

      cur = self._connect_get_cursor()

      columns = ', '.join([f'{k} = ?' for k in data.keys()])

      cur.execute(f"UPDATE {self._table} SET {columns} WHERE id = ?", (*data.values(), id_num, ))
      self._connection.commit()

      return cur.rowcount > 0
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      self._disconnect()

  def delete(self, id_num: int) -> bool:
    """ Delete entry (soft delete).

    Parameters:
      id_num (int): unique id for the entry to delete

    Returns:
      boolean:      True if item chaned, False otherwise

    Raises:
      Exception:    In case of any error
    """
    try:
      cur = self._connect_get_cursor()

      cur.execute(f"UPDATE {self._table} SET deleted = CURRENT_TIMESTAMP WHERE id = ?", (id_num, ))
      self._connection.commit()

      return cur.rowcount > 0
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      self._disconnect()

  def _get_column_names(self) -> list[str]:
    """ Get column names of the table.

    Returns:
      list[str]:    A list of column names

    Raises:
      Exception:    In case of any error
    """
    try:
      cur = self._connect_get_cursor()
      cur.execute(f"PRAGMA table_info ({self._table})")
      columns_info = cur.fetchall()

      return [info[1] for info in columns_info]
    except Exception as err:
      raise err
    finally:
      self._disconnect()

  def _control_keys(self, keys: list[any]) -> None:
    """Controls keys from user input with columns in database. Raises error if not valid or key is id.

    Paramters:
      keys (list[str]):       List of keys to control.

    Raises:
      KeyUnmutableException:  in case key is not valid
    """
    column_names = self._get_column_names()

    for key in keys:  # Control keys for sql-injection
      if str(key) not in column_names or str(key) == "id":
        raise KeyUnmutableException("Key for column not valid.")