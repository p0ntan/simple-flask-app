"""
DAO is used for simplyfying handling with data from database.
"""

import os
import sqlite3
from contextlib import contextmanager
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
        self._db_path = os.environ.get("SQLITE_PATH", "./db/db.sqlite")
        self._table = table_name
        self._connection = None

    def _get_connection(self) -> sqlite3.Connection:
        """Connect to the sqlite database and get connection.

        Returns:
          connection:   To use for executing queries
        """
        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        self._connection = connection

        return self._connection

    def _disconnect(self):
        """Disconnects the connection."""
        if self._connection is not None:
            self._connection.close()

        self._connection = None

    @contextmanager
    def _get_db_connection(self):
        """Creates a context for all connections for dao.

        Centralizes the connection, commit, rollback and disconnection to keep code DRY.

        Raises:
          Exception:  In case of any error
        """
        conn = None

        try:
            conn = self._get_connection()
            yield conn
            conn.commit()
        except Exception as err:
            if conn is not None:
                conn.rollback()
            printer.print_fail(err)
            raise err
        finally:
            self._disconnect()

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
        with self._get_db_connection() as conn:
            columns = ", ".join([f"{k} = ?" for k in data.keys()])
            res = conn.execute(
                f"UPDATE {self._table} SET {columns} WHERE id = ?",
                (
                    *data.values(),
                    id_num,
                ),
            )

            return res.rowcount > 0

    def delete(self, id_num: int) -> bool:
        """Delete entry from database (soft delete).

        Args:
          id_num (int): unique id for the entry to delete

        Returns:
          boolean:      True if item deleted, False otherwise

        Raises:
          Exception:    In case of any error
        """
        with self._get_db_connection() as conn:
            res = conn.execute(
                f"UPDATE {self._table} SET deleted = CURRENT_TIMESTAMP WHERE id = ?",
                (id_num,),
            )

            return res.rowcount > 0
