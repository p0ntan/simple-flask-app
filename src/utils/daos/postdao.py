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

  def get_post_and_users_with_pagination(self, topic_id: int, pagnation: int = 0) -> list[dict[str, Any]]:
    """Gets post for a certain topic, with pagination for the posts.

    Args:
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
      """, (topic_id, pagnation * 10))
      column_names = [description[0] for description in cur.description]

      posts_data = [dict(zip(column_names, row)) for row in rows]

      for post in posts_data:
        author = {
            "user_id": post.pop("user_id"),
            "username": post.pop("username"),
            "role": post.pop("role"),
            "signature": post.pop("signature"),
            "avatar": post.pop("avatar")
        }
        post["author"] = author

      return posts_data
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      self._disconnect()

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
    conn = None

    try:
      conn, cur = self._get_connection_and_cursor()
      cur.execute(self.GET_ONE_QUERY, (id_num, ))
      result = cur.fetchone()

      if result is None:
        return result

      column_names = [description[0] for description in cur.description]
      post_data = dict(zip(column_names, result))

      author = {
        "user_id": post_data.pop("user_id"),
        "username": post_data.pop("username"),
        "role": post_data.pop("role"),
        "signature": post_data.pop("signature"),
        "avatar": post_data.pop("avatar")
      }
      post_data["author"] = author

      return PostData(**post_data)
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()

  def create(self, data: dict[str, str | int]) -> PostData:
    """Create (insert) a new post into database.

    Args:
      data (dict):      The data for the new post.

    Returns:
      PostData (dict):  The new post, with userdata.

    Raises:
      Exception:        in case of any error like unique entry already exist.
    """
    conn = None

    try:
      conn, cur = self._get_connection_and_cursor()
      cur.execute("""
        INSERT INTO post
          (author, topic_id, title, body)
        VALUES
          (?, ?, ?, ?)          
      """,
      (data["author"], data["topic_id"],data.get("title", None), data["body"]))
      conn.commit()

      cur.execute(self.GET_ONE_QUERY, (cur.lastrowid, ))
      result = cur.fetchone()
      column_names = [description[0] for description in cur.description]

      post_data = dict(zip(column_names, result))
      author = {
        "user_id": post_data.pop("user_id"),
        "username": post_data.pop("username"),
        "role": post_data.pop("role"),
        "signature": post_data.pop("signature"),
        "avatar": post_data.pop("avatar")
      }
      post_data["author"] = author

      return PostData(**post_data)
    except Exception as err:
      printer.print_fail(err)
      raise err
    finally:
      if conn is not None:
        conn.close()
  
  def get_posts_and_topic(self, topic_id: int, pagnation: int = 0) -> dict:
    """ Gets topic and posts for that topic.

    Args:
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
