import os
import sqlite3
base_dir = os.path.dirname(__file__)

class DAO:
  def __init__(self, table_name: str):
    self.db_path = os.environ.get(
      "SQLITE_PATH",
      os.path.join(base_dir, "../db/db.sqlite")
    )
    self.table = table_name
    self._connection = None

  def _connect_get_cursor(self) -> sqlite3.Cursor:
    """
    Connect to the sqlite database. 
    
    returns:
      sqlite3 cursor
    """
    self._connection = sqlite3.connect(self.db_path)
    return self._connection.cursor()

  def _disconnect(self):
    """ Disconnects the connection. """
    self._connection.close()

  def get_all(self) -> list[dict]:
    """
    Get all data from table.
    
    returns:
      list[dict] -- A list with dictionaries with all data
    
    raises:
      Exception -- in case of any error
    """
    try:
      cur = self._connect_get_cursor()
      
      rows = cur.execute(f"SELECT * FROM {self.table}")
      column_names = [description[0] for description in cur.description]

      result = [dict(zip(column_names, row)) for row in rows]
      self._disconnect()

      return result
    except Exception as err:
      print(err)
      raise err

  def get_one(self, id: int) -> dict | None:
    """
    Get one entry

    returns:
      dict -- with data from single entry
      None -- if no entry found with given id
    
    raises:
      Exception -- in case of any error
    """
    try:
      cur = self._connect_get_cursor()
      
      cur.execute(f"SELECT * FROM {self.table} WHERE id = ?", (id, ))
      column_names = [description[0] for description in cur.description]

      result = cur.fetchone()

      if result is not None:
        result = dict(zip(column_names, result))

      self._disconnect()

      return result
    except Exception as err:
      print(err)
      raise err
