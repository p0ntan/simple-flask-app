from abc import ABC, abstractmethod

class Controller(ABC):
  @abstractmethod
  def create(self, data: dict) -> int:
    """ Create entry. """

  @abstractmethod
  def get_all(self) -> list[dict]:
    """ Get all entries. """

  @abstractmethod
  def get_one(self, id: int) -> dict:
    """ Get one entry. """

  @abstractmethod
  def update(self, id: int, data: dict) -> bool:
    """ Get update entry. """
  
  @abstractmethod
  def delete(self, id: int) -> bool:
    """ Delete entry. """
