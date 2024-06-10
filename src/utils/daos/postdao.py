"""
PostDAO is used for access posts.
"""
from src.utils.daos.dao import DAO
from typing import Any
from src.utils.print_colors import ColorPrinter

printer = ColorPrinter()


class PostDAO(DAO):
  """ PostDAO for accessing posts. """

  def __init__(self, table_name: str):
    super().__init__(table_name=table_name)

  def get_post_and_users_with_pagination(self, topic_id: int, pagnation: int = 0) -> list[dict[str, Any]]:
    """ Gets post for a certain topic, with pagination for the posts.

    Parameters:
      topic_id(int):    the id for the topic
      pagnationn(int):  pages in, 0 = first 10

    Returns:
      list:             with posts as dictionaries

    Raises:
      Exception:    in case of any error
    """
    try:
      cur = self._connect_get_cursor()

      rows = cur.execute("""
        SELECT 
          post.id AS post_id,
          post.topic_id,
          post.created,
          post.last_edited,
          post.title,
          post.body,
          user.username,
          user.signature,
          user.avatar
        FROM post
        JOIN user ON post.user_id = user.id
        WHERE post.topic_id = ? AND post.deleted IS NULL
        ORDER BY post.created ASC
        LIMIT 10
        OFFSET ?
      """, (topic_id, pagnation * 10))
      column_names = [description[0] for description in cur.description]

      posts = [dict(zip(column_names, row)) for row in rows]

      for post in posts:
        author = {
            "username": post.pop("username"),
            "signature": post.pop("signature"),
            "avatar": post.pop("avatar")
        }
        post["author"] = author

      return posts
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      self._disconnect()


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
