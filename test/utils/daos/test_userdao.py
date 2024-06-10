import os
import pytest
import sqlite3
import unittest.mock as mock
from src.utils.daos.userdao import UserDAO, UserData

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

  with mock.patch("src.utils.daos.dao.os.environ.get") as db_path:
    db_path.return_value = test_db
    sut = UserDAO()
    yield sut
    os.remove(test_db)



@pytest.mark.integration
class TestIntegrationUserDAO:
  """Integration tests."""

  @pytest.mark.parametrize("user_name, expected_user_type", [
    ("admin", dict),
    ("nonexistent_user", type(None)),
  ])
  def test_get_user_by_name_type(self, sut_int, user_name, expected_user_type):
    """Test that get_user_by_name returns the correct type."""
    user = sut_int.get_user_by_username(user_name)

    assert isinstance(user, expected_user_type)

  @pytest.mark.parametrize("username, expected_user", [
    ("admin", {"user_id": 1, "username": "admin", "role": "admin", "signature": None, "avatar": None}),
    ("johndoe", {"user_id": 5, "username": "johndoe", "role": "author", "signature": None, "avatar": None}),
  ])
  def test_get_user_by_username(self, sut_int, username, expected_user):
    """Test to get user by username by controlling data."""
    user = sut_int.get_user_by_username(username)

    assert user == expected_user
