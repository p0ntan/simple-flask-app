"""
Baseclass for all controllers.

Note that there are no try/except here. Instead these should be catched in the method used in as controller.
"""
from src.utils.daos.dao import DAO
from src.errors.customerrors import NoDataException


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
    """
    return self._dao.create(data)

  def get_all(self) -> list[dict]:
    """ Get all entries.

    Returns:
      list[dict]:   List with all entires
    """
    return self._dao.get_all()

  def get_one(self, id_num: int) -> dict:
    """ Get one entry.

    Parameters:
      id_num (int): unique id for the entry to get

    Returns:
      dict:         with data from entry

    Raises:
      NoDataException: if no data is found for the given id
    """
    data = self._dao.get_one(id_num)

    if data is None:
      raise NoDataException(f"No data found for given id: {id_num}")

    return data

  def update(self, id_num: int, data: dict) -> bool:
    """ Update existing entry.

    Parameters:
      id_num (int): unique id for the entry to update
      data (dict):  dictionary with new data

    Returns:
      True:         True if entry updated

    Raises:
      NoDataException: if no data is found for the given id
    """
    success = self._dao.update(id_num, data)

    if not success:
      raise NoDataException(f"No data found for given id: {id_num}.")

    return success

  def delete(self, id_num: int) -> bool:
    """ Delete entry.

    Parameters:
      id_num (int): unique id for the entry to delete.

    Returns:
      boolean:      True if entry deleted

    Raises:
      NoDataException: if no data is found for the given id
    """
    success = self._dao.delete(id_num)

    if not success:
      raise NoDataException(f"Data not deleted with id {id_num}")

    return success
