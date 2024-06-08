"""
PostDAO is used for access posts.
"""
from src.utils.daos.dao import DAO
from src.utils.print_colors import ColorPrinter

printer = ColorPrinter()


class PostDAO(DAO):
  """ PostDAO for accessing posts. """

  def __init__(self, table_name: str):
    super().__init__(table_name=table_name)

  def get_posts_and_topic(self, topic_id: int, pagnation: int = 0) -> dict:
    """ Gets topic and posts for that topic.

    Parameters:
      topic_id(int):    the id for the topic
      pagnationn(int):  pages in, 0 = first 10

    Returns:
      dict:             with data in keys topic and posts

    Raises:
      Exception:    in case of any error
    """
    try:
      cur = self._connect_get_cursor()

      rows = cur.execute("SELECT * FROM topic WHERE id = ?", (topic_id, ))
      column_names = [description[0] for description in cur.description]

      topic = [dict(zip(column_names, row)) for row in rows]

      rows = cur.execute("""
        SELECT * FROM post
        WHERE topic_id = ? AND deleted IS NULL
        ORDER BY created ASC
        LIMIT 10
        OFFSET ?
      """, (topic_id, pagnation * 10))
      column_names = [description[0] for description in cur.description]

      posts = [dict(zip(column_names, row)) for row in rows]

      return {"topic": topic, "posts": posts}
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      self._disconnect()
