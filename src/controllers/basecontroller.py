"""
Abstract class for all controllers.

They should all have create, get_one, update and delete methods.
"""
from abc import ABC, abstractmethod
from flask import Response


class Controller(ABC):
  """Abstract class for controllers."""

  @abstractmethod
  def create(self) -> tuple[Response, int]:
    """Create a new entry."""

  @abstractmethod
  def get_one(self, id_num: int) -> tuple[Response, int]:
    """Get one entry."""

  @abstractmethod
  def update(self, id_num: int) -> tuple[Response, int]:
    """Update existing entry."""

  @abstractmethod
  def delete(self, id_num: int) -> tuple[Response, int]:
    """ Delete entry."""
