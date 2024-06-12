import os
import re
import pytest
import sqlite3
import unittest.mock as mock
from src.utils.daos.postdao import PostDAO

base_dir = os.path.dirname(__file__)
test_db = os.path.join(base_dir, "test_data/test_db.sqlite")

@pytest.fixture
def sut_int():
  """SUT for integrationtest."""
  test_data = os.path.join(base_dir, "test_data/insert.sql")
  files = ["./db/ddl.sql", test_data]

  conn = sqlite3.connect(test_db)
  cursor = conn.cursor()

  for file in files:
    with open(file, 'r') as f:
        sql_commands = f.read()
        cursor.executescript(sql_commands)

  conn.commit()
  conn.close()

  with mock.patch("src.utils.daos.basedao.os.environ.get") as db_path:
    db_path.return_value = test_db
    sut = PostDAO("post")
    yield sut
    os.remove(test_db)


@pytest.mark.integration
class TestIntegrationPostDAO:
  """Integration tests."""

  @pytest.mark.parametrize("id, expected",[
    (1, True),
    (200, False),
  ])
  def test_delete(self, sut_int, id, expected):
    """Test return value when updating a user."""
    result = sut_int.delete(id)

    assert result == expected

  @pytest.mark.parametrize("id",[
    (1),
  ])
  def test_delete_data(self, sut_int, id):
    """Test data when updating a user."""
    result = sut_int.delete(id)

    conn = sqlite3.connect(test_db)
    cur = conn.cursor()
    cur.execute("SELECT deleted from post where id = ?", (id, ))
    result = cur.fetchone()

    conn.close()

    assert re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", result[0])

  @pytest.mark.parametrize("topic_id, page, expected_posts",[
    (1, 0, 10),
    (1, 1, 4),
    (4, 0, 2),
    (2, 0, 0),
  ])
  def test_get_post_and_topic(self, sut_int, topic_id, page, expected_posts):
    """Test get topic and posts, check amount."""
    data = sut_int.get_posts_and_topic(topic_id, page)

    assert len(data["posts"]) == expected_posts
  
  @pytest.mark.parametrize("topic_id, page, expected_first, expected_last",[
    (1, 0, "Has no title", "Is the last of first ten"),
    (1, 1, "Is the first of second ten.", "Is the last of second ten."),
  ])
  def test_get_post_and_topic_last_body(self, sut_int, topic_id, page, expected_first, expected_last):
    """Test get topic and posts, check last body message."""
    data = sut_int.get_posts_and_topic(topic_id, page)

    assert data["posts"][0]["body"] == expected_first and data["posts"][-1]["body"] == expected_last
