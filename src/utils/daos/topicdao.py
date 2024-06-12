"""
TopicDAO is used for accessing users.
"""
from __future__ import annotations
from typing import Any
from src.utils.daos.basedao import DAO
from src.utils.print_colors import ColorPrinter
from src.static.types import TopicData

printer = ColorPrinter()


class TopicDAO(DAO):
  """ TopicDAO for accessing posts. """
  GET_ONE_QUERY = """
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
    WHERE topic.id = ?
    AND topic.deleted IS NULL
  """

  def __init__(self, table_name: str):
    super().__init__(table_name)

  def create(self, data: dict[str, str | int]) -> TopicData:
    """ Create (insert) a new entry into database.

    Parameters:
      data (dict):      The data for the new topic.

    Returns:
      TopicData (dict): The new topic, with userdata.

    Raises:
      Exception:        in case of any error like unique entry already exist.
    """
    conn = None

    try:
      conn, cur = self._get_connection_and_cursor()
      cur.execute("""
        INSERT INTO topic
          (created_by, title, category)
        VALUES
          (?, ?, ?)          
      """,
      (data["created_by"], data["title"], data["category"]))
      conn.commit()

      cur.execute(self.GET_ONE_QUERY, (cur.lastrowid, ))
      result = cur.fetchone()
      column_names = [description[0] for description in cur.description]

      topic_dict = dict(zip(column_names, result))

      return TopicData(**topic_dict)
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()

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
    conn = None
    try:
      conn, cur = self._get_connection_and_cursor()

      columns = ', '.join([f'{k} = ?' for k in data.keys()])

      cur.execute(f"UPDATE topic SET {columns} WHERE id = ?", (*data.values(), id_num, ))
      conn.commit()

      return cur.rowcount > 0
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()

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
    conn = None

    try:
      conn, cur = self._get_connection_and_cursor()
      cur.execute(self.GET_ONE_QUERY, (id_num, ))
      result = cur.fetchone()

      if result is None:
        return result

      column_names = [description[0] for description in cur.description]
      topic_data = dict(zip(column_names, result))

      created_by = {
        "user_id": topic_data.pop("user_id"),
        "username": topic_data.pop("username"),
        "role": topic_data.pop("role"),
        "signature": topic_data.pop("signature"),
        "avatar": topic_data.pop("avatar"),
      }
      topic_data["created_by"] = created_by

      return TopicData(**topic_data)
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()

  def delete(self, id_num: int) -> bool:
    """Delete topic from database (soft delete).

    Args:
      id_num (int): unique id for the topic to delete

    Returns:
      boolean:      True if item deleted, False otherwise

    Raises:
      Exception:    In case of any error
    """
    conn = None
    try:
      conn, cur = self._get_connection_and_cursor()
      # TODO add soft delete for users topic and posts, with same timestamp?
      cur.execute(f"UPDATE topic SET deleted = CURRENT_TIMESTAMP WHERE id = ?", (id_num, ))
      conn.commit()

      return cur.rowcount > 0
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()
