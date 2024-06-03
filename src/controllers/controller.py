"""
Baseclass for all controllers.
"""
from src.utils.dao import DAO


class Controller:
  """ Baseclass for all Controllers. A very general way for accessing data. """
  def __init__(self, dao: DAO):
    self._dao = dao

  def create(self, data: dict) -> dict:
    """ Create a new entry.

    Parameters:
      data (dict):  dictionary with data

    Returns:
      dict:         data for the new entry with id.
      None:         In case of any failure.
    """
    try:
      return self._dao.create(data)
    except Exception:
      return None

  def get_all(self) -> list[dict]:
    """ Get all entries.

    Returns:
      list[dict]:   List with all entires
    """
    try:
      return self._dao.get_all()
    except Exception:
      return []

  def get_one(self, id_num: int) -> dict:
    """ Get one entry.

    Parameters:
      id_num (int): unique id for the entry to get

    returns:
      dict:         with data from entry
      None:         if no match
    """
    try:
      return self._dao.get_one(id_num)
    except Exception:
      return None

  def update(self, id_num: int, data: dict) -> bool:
    """ Update existing entry.

    Parameters:
      id_num (int): unique id for the entry to update
      data (dict):  dictionary with new data

    Returns:
      boolean:      True if entry updated, False otherwise
    """
    try:
      return self._dao.update(id_num, data)
    except Exception:
      return False

  def delete(self, id_num: int) -> bool:
    """ Delete entry.

    Parameters:
      id_num (int): unique id for the entry to delete.

    Returns:
      boolean:      True if entry deleted, False otherwise
    """
    try:
      return self._dao.delete(id_num)
    except Exception:
      return False
