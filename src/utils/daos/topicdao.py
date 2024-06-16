"""
TopicDAO is used for accessing users.
"""

from __future__ import annotations
from src.utils.daos.basedao import DAO
from src.utils.print_colors import ColorPrinter
from src.static.types import TopicData

printer = ColorPrinter()


class TopicDAO(DAO):
    """TopicDAO for accessing posts."""

    GET_ONE_QUERY = """
    SELECT
      topic.id AS topic_id,
      topic.title,
      topic.category,
      topic.created,
      topic.last_edited,
      topic.deleted,
      topic.disabled,
      (SELECT COUNT(id) FROM post WHERE post.topic_id = topic.id AND post.deleted IS NULL) as no_of_posts,
      user.id as user_id,
      user.username,
      user.role,
      user.signature,
      user.avatar
    FROM topic
    JOIN user ON topic.created_by = user.id
    WHERE topic.id = ?
    AND topic.deleted IS NULL
  """

    def __init__(self, table_name: str):
        super().__init__(table_name)

    def create(self, data: dict[str, str | int]) -> TopicData:
        """Create (insert) a new entry into database.

        Parameters:
          data (dict):      The data for the new topic.

        Returns:
          TopicData (dict): The new topic, with userdata.

        Raises:
          Exception:        in case of any error like unique entry already exist.
        """
        with self._get_db_connection() as conn:
            res = conn.execute(
                """
        INSERT INTO topic
          (created_by, title, category)
        VALUES
          (?, ?, ?)
      """,
                (data["created_by"], data["title"], data["category"]),
            )

            result = conn.execute(self.GET_ONE_QUERY, (res.lastrowid,)).fetchone()

            return TopicData(**result)

    def update(self, id_num: int, data: dict) -> bool:
        """Update topic.

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
                f"UPDATE topic SET {columns} WHERE id = ?",
                (
                    *data.values(),
                    id_num,
                ),
            )

            return res.rowcount > 0

    def get_one(self, id_num: int) -> TopicData | None:
        """Get one topic from database.

        Args:
          id_num (int):     unique id for the topic.

        Returns:
          TopicData (dict): with data from single topic
          None:             if no entry found with given id

        Raises:
          Exception:        in case of any error
        """
        with self._get_db_connection() as conn:
            result = conn.execute(self.GET_ONE_QUERY, (id_num,)).fetchone()

            if result is None:
                return result

            topic_data = dict(result)

            created_by = {
                "user_id": topic_data.pop("user_id"),
                "username": topic_data.pop("username"),
                "role": topic_data.pop("role"),
                "signature": topic_data.pop("signature"),
                "avatar": topic_data.pop("avatar"),
            }
            topic_data["created_by"] = created_by

            return TopicData(**topic_data)

    def delete(self, id_num: int) -> bool:
        """Delete topic from database (soft delete) by setting deleted to current time.

        Args:
          id_num (int): unique id for the topic to delete

        Returns:
          boolean:      True if item deleted, False otherwise

        Raises:
          Exception:    In case of any error
        """
        with self._get_db_connection() as conn:
            # TODO add soft delete for users, topic and posts, with same timestamp?
            res = conn.execute(
                "UPDATE topic SET deleted = CURRENT_TIMESTAMP WHERE id = ?", (id_num,)
            )

            return res.rowcount > 0

    def get_latest_topics(self, limit: int) -> list[TopicData]:
        """Get the latest topics in the database, based on creation date.

        Returns:
          list[TopicData]: The list of topics.
        """
        with self._get_db_connection() as conn:
            results = conn.execute(
                """
        SELECT
          topic.id AS topic_id,
          topic.title,
          topic.category,
          topic.created,
          topic.last_edited,
          topic.deleted,
          topic.disabled,
          user.id as user_id,
          user.username,
          user.role,
          user.signature,
          user.avatar
        FROM topic
        JOIN user ON topic.created_by = user.id
        WHERE topic.deleted IS NULL
        ORDER BY created DESC
        LIMIT ?
      """,
                (limit,),
            )

            topics_data: list[TopicData] = []

            for topic in results:
                topic_data = dict(topic)
                topic_data["created_by"] = {
                    "user_id": topic_data.pop("user_id"),
                    "username": topic_data.pop("username"),
                    "role": topic_data.pop("role"),
                    "signature": topic_data.pop("signature"),
                    "avatar": topic_data.pop("avatar"),
                }
                topics_data.append(TopicData(**topic_data))

            return topics_data
