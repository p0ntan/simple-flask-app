from src.utils.dao import DAO

class Controller:
  def __init__(self, dao: DAO):
    self._dao = dao

  def create(self, data: dict) -> dict | None:
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

  def get_one(self, id: int) -> dict | None:
    """ Get one entry.
    
    returns:
      dict:         with data from entry
      None:         if no match
    """
    try:
      return self._dao.get_one(id)
    except Exception:
      return None

  def update(self, id: int, data: dict) -> bool:
    """ Update existing entry.
    
    Parameters:
      id (int):     unique id for the entry to update 
      data (dict):  dictionary with new data 
    
    Returns:
      boolean:      True if entry updated, False otherwise
    """
    try:
      return self._dao.update(id, data)
    except Exception:
      return False

  def delete(self, id: int) -> bool:
    """ Delete entry.
    
    Parameters:
      id (int):     unique id for the entry to delete.

    Returns:
      boolean:      True if entry deleted, False otherwise
    """
    try:
      return self._dao.delete(id)
    except Exception:
      return False
