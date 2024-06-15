"""
PostDAO is used for access posts.
"""

from src.utils.daos.basedao import DAO
from typing import Any
from src.static.types import PostData
from src.utils.print_colors import ColorPrinter

printer = ColorPrinter()


class PostDAO(DAO):
    """PostDAO for accessing posts."""

    GET_ONE_QUERY = """
    SELECT
      post.id AS post_id,
      post.topic_id,
      post.created,
      post.last_edited,
      post.title,
      post.body,
      user.id as user_id,
      user.username,
      user.role,
      user.signature,
      user.avatar
    FROM post
    JOIN user ON post.author = user.id
    WHERE post.id = ?
    AND post.deleted IS NULL
    """

    def __init__(self, table_name: str):
        super().__init__(table_name)

    def get_post_and_users_with_pagination(
        self, topic_id: int, pagnation: int = 0
    ) -> list[dict[str, Any]]:
        """Gets post for a certain topic, with pagination for the posts.

        Args:
          topic_id(int):    the id for the topic
          pagnationn(int):  pages in, 0 = first 10

        Returns:
          list:             with posts as dictionaries

        Raises:
          Exception:    in case of any error
        """
        with self._get_db_connection() as conn:
            results = conn.execute(
                """
        SELECT
          post.id AS post_id,
          post.topic_id,
          post.created,
          post.last_edited,
          post.title,
          post.body,
          user.id as user_id,
          user.username,
          user.role,
          user.signature,
          user.avatar
        FROM post
        JOIN user ON post.author = user.id
        WHERE post.topic_id = ? AND post.deleted IS NULL
        ORDER BY post.created ASC
        LIMIT 10
        OFFSET ?
      """,
                (topic_id, pagnation * 10),
            ).fetchall()

            post_data = []

            for row in results:
                post = dict(row)
                author = {
                    "user_id": post.pop("user_id"),
                    "username": post.pop("username"),
                    "role": post.pop("role"),
                    "signature": post.pop("signature"),
                    "avatar": post.pop("avatar"),
                }
                post["author"] = author
                post_data.append(post)

            return post_data

    def get_one(self, id_num: int) -> PostData | None:
        """Get one post from database.

        Args:
          id_num (int):     unique id for the post.

        Returns:
          PostData (dict):  with data from single post
          None:             if no post found with given id

        Raises:
          Exception:        in case of any error
        """
        with self._get_db_connection() as conn:
            result = conn.execute(self.GET_ONE_QUERY, (id_num,)).fetchone()

            if result is None:
                return result

            post_data = dict(result)
            post_data["author"] = {
                "user_id": post_data.pop("user_id"),
                "username": post_data.pop("username"),
                "role": post_data.pop("role"),
                "signature": post_data.pop("signature"),
                "avatar": post_data.pop("avatar"),
            }

            return PostData(**post_data)

    def create(self, data: dict[str, str | int]) -> PostData:
        """Create (insert) a new post into database.

        Args:
          data (dict):      The data for the new post.

        Returns:
          PostData (dict):  The new post, with userdata.

        Raises:
          Exception:        in case of any error like unique entry already exist.
        """
        with self._get_db_connection() as conn:
            res = conn.execute(
                """
        INSERT INTO post
          (author, topic_id, title, body)
        VALUES
          (?, ?, ?, ?)
      """,
                (
                    data["author"],
                    data["topic_id"],
                    data.get("title", None),
                    data["body"],
                ),
            )

            result = conn.execute(self.GET_ONE_QUERY, (res.lastrowid,)).fetchone()
            post_data = dict(result)
            post_data["author"] = {
                "user_id": post_data.pop("user_id"),
                "username": post_data.pop("username"),
                "role": post_data.pop("role"),
                "signature": post_data.pop("signature"),
                "avatar": post_data.pop("avatar"),
            }

            return PostData(**post_data)
