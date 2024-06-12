"""
Base service, should be inherited by all services that is used in base_controller.
"""

from abc import ABC, abstractmethod
from typing import Any

class BaseService(ABC):
  """
  Base service, should be inherited by all services that is used in base_controller.
  """

  @abstractmethod
  def __init__(self, *args, **kwargs) -> None:
    """Initializes the BaseService class."""

  @abstractmethod
  def create(self, *args, **kwargs) -> Any:
    """Creates a new item in the database."""

  @abstractmethod
  def get_by_id(self, *args, **kwargs) -> Any:
    """Gets one item from the database."""

  @abstractmethod
  def update(self, *args, **kwargs) -> bool:
    """Updates an item in the database."""

  @abstractmethod
  def delete(self, *args, **kwargs) -> bool:
    """Deletes an item in the database."""
