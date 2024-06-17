"""
UserDAO is used for accessing users.
"""

from __future__ import annotations
from src.static.types import UserData
from src.utils.daos.basedao import DAO
from src.utils.print_colors import ColorPrinter

printer = ColorPrinter()


class UserDAO(DAO):
    """UserDAO for accessing posts."""

    GET_ONE_QUERY_USERNAME = "SELECT id AS user_id, username, role, signature, avatar FROM user WHERE username = ?"
    GET_ONE_QUERY_ID = (
        "SELECT id as user_id, username, role, signature, avatar FROM user WHERE id = ?"
    )

    def __init__(self, table_name: str):
        super().__init__(table_name)

    def create(self, data: dict[str, str]) -> UserData:
        """Create (insert) a new entry into database.

        Parameters:
          data (dict):  The data for the new user.

        Returns:
          UserData:     Dictonary with the new user.

        Raises:
          Exception:    in case of any error like unique entry already exist.
        """
        with self._get_db_connection() as conn:
            res = conn.execute(
                "INSERT INTO user (username) VALUES (?)", (data["username"],)
            )
            user_data = conn.execute(self.GET_ONE_QUERY_ID, (res.lastrowid,)).fetchone()

            return UserData(**user_data)

    def get_user_by_username(self, username: str) -> UserData | None:
        """Retrieves a user from the database by their username.

        Parameters:
          username (str): The username of the user to retrieve.

        Returns:
          UserData:       Dictonary with the user.
          None:           None if not found.

        Raises:
          Exception:      If an error occurs while retrieving the user.
        """
        with self._get_db_connection() as conn:
            result = conn.execute(self.GET_ONE_QUERY_USERNAME, (username,)).fetchone()

            if result is None:
                return result

            return UserData(**result)

    def get_one(self, id_num: int) -> UserData | None:
        """Retrieves a user from the database by their id.

        Parameters:
          id_num (int): The id of the user to retrieve.

        Returns:
          UserData:     Dictonary with the user.
          None:         None if not found.

        Raises:
          Exception:    If an error occurs while retrieving the user.
        """
        with self._get_db_connection() as conn:
            result = conn.execute(self.GET_ONE_QUERY_ID, (id_num,)).fetchone()

            if result is None:
                return result

            return UserData(**result)

    def get_permission_from_role(self, role: str) -> dict[str, str | bool]:
        """Retrieves a roles permissions based on name (admin, moderator, author).

        Parameters:
          role (str):   The role to get the permissions from.

        Returns:
          roles (dict): Dictonary with the roles.
          None:         If no result for role

        Raises:
          Exception:    If an error occurs while retrieving the user.
        """
        with self._get_db_connection() as conn:
            result = conn.execute(
                "SELECT * FROM permission WHERE role = ?"
                ,(role,)).fetchone()

            if result is None:
                return result

            return dict(result)
