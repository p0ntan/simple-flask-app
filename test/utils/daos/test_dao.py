# import os
# import re
# import pytest
# import sqlite3
# import unittest.mock as mock
# from src.utils.daos.basedao import DAO
# from src.errors.customerrors import KeyUnmutableException

# base_dir = os.path.dirname(__file__)
# test_db = os.path.join(base_dir, "test_data/test_db.sqlite")
# faked_rows = ((1, "johndoe", "author"), (2, "admin", "admin"), (3, "elmapelma", "moderator"))
# faked_names = (("id",), ("username", ), ("role", ))
# faked_expected = [
#   {
#     "id": 1,
#     "username": "johndoe",
#     "role": "author"
#   },
#   {
#     "id": 2,
#     "username": "admin",
#     "role": "admin"
#   },
#   {
#     "id": 3,
#     "username": "elmapelma",
#     "role": "moderator"
#   },
# ]

# @pytest.fixture
# def sut_int(table_name: str):
#   """SUT for integrationtest."""
#   test_data = os.path.join(base_dir, "test_data/insert.sql")
#   files = ["./db/ddl.sql", test_data]

#   conn = sqlite3.connect(test_db)
#   cursor = conn.cursor()

#   for file in files:
#     with open(file, 'r') as f:
#         sql_commands = f.read()
#         cursor.executescript(sql_commands)

#   conn.commit()
#   conn.close()

#   with mock.patch("src.utils.daos.dao.os.environ.get") as db_path:
#     db_path.return_value = test_db
#     sut = DAO(table_name)
#     yield sut
#     os.remove(test_db)

# @pytest.fixture
# def sut():
#   """SUT for unittest."""
#   sut = DAO("")

#   return sut

# @pytest.mark.unit
# class TestUnitDAO:
#   @pytest.mark.parametrize("result, names, expected", [
#     ((2, "admin", "admin"),faked_names, {
#       "id": 2,
#       "username": "admin",
#       "role": "admin"
#     }),
#     (None, faked_names, None)
#   ])
#   @mock.patch("src.utils.daos.dao.DAO._connect_get_cursor", autospec=True)
#   @mock.patch("src.utils.daos.dao.DAO._disconnect", autospec=True)
#   def test_get_one(self, mockedDisconnect, mockedCGC, sut, result, names, expected):
#     """
#     Get one
#     """
#     mocked_cursor = mock.MagicMock()
#     mocked_cursor.description = names
#     mocked_cursor.fetchone.return_value = result

#     mockedCGC.return_value = mocked_cursor
#     mockedDisconnect.side_effect = None

#     result = sut.get_one(2)

#     assert result == expected

#   @mock.patch("src.utils.daos.dao.DAO._connect_get_cursor", autospec=True)
#   def test_get_one_exception(self, mockedCGC, sut):
#     """
#     Get one - exception
#     """
#     mocked_cursor = mock.MagicMock()
#     mocked_cursor.fetchone.side_effect = Exception
#     mockedCGC.return_value = mocked_cursor

#     with pytest.raises(Exception):
#       sut.get_one(2)

#   @pytest.mark.parametrize("rows, names, expected", [
#     (faked_rows,(("id",), ("username", ), ("role", )), faked_expected),
#     ([], (("id",), ("username", ), ("role", )), [])
#   ])
#   @mock.patch("src.utils.daos.dao.DAO._connect_get_cursor", autospec=True)
#   @mock.patch("src.utils.daos.dao.DAO._disconnect", autospec=True)
#   def test_get_all(self, mockedDisconnect, mockedCGC, sut, rows, names, expected):
#     """
#     Get all
#     """
#     mocked_cursor = mock.MagicMock()
#     mocked_cursor.execute.return_value = rows
#     mocked_cursor.description = names

#     mockedCGC.return_value = mocked_cursor
#     mockedDisconnect.side_effect = None

#     result = sut.get_all()

#     assert result == expected

#   @mock.patch("src.utils.daos.dao.DAO._connect_get_cursor", autospec=True)
#   def test_get_all_exception(self, mockedCGC, sut):
#     """
#     Get all - exception
#     """
#     mocked_cursor = mock.MagicMock()
#     mocked_cursor.execute.side_effect = Exception
#     mockedCGC.return_value = mocked_cursor

#     with pytest.raises(Exception):
#       sut.get_all()

#   @mock.patch("src.utils.daos.dao.DAO._control_keys", autospec=True)
#   @mock.patch("src.utils.daos.dao.DAO._disconnect", autospec=True)
#   def test_update_exception(self, mocked_DC, mockedCK, sut):
#     """Test that when an exception is raised the _disconnect in finally block is called."""
#     mockedCK.side_effect = KeyUnmutableException("Key for column not valid.")

#     with pytest.raises(KeyUnmutableException):
#       sut.update(2, {})
#     mocked_DC.assert_called_once()

#   @mock.patch("src.utils.daos.dao.DAO._connect_get_cursor", autospec=True)
#   @mock.patch("src.utils.daos.dao.DAO._disconnect", autospec=True)
#   def test_delete_exception(self, mocked_DC, mockedCGC, sut):
#     """Test that when an exception is raised the _disconnect in finally block is called."""
#     mockedCGC.side_effect = Exception

#     with pytest.raises(Exception):
#       sut.delete(2)
#     mocked_DC.assert_called_once()

#   @pytest.mark.parametrize("keys", [
#     (["topic", "name", "fail"]),
#     (["id"])
#   ])
#   @mock.patch("src.utils.daos.dao.DAO._get_column_names", autospec=True)
#   def test_control_keys_fail(self, mockedGCN, sut, keys):
#     """Test that control keys raises exception."""
#     mockedGCN.return_value = ["topic", "name", "body"]

#     with pytest.raises(KeyUnmutableException):
#       sut._control_keys(keys)

#   @pytest.mark.parametrize("keys", [
#     (["topic", "name", "body"]),
#     (["name"]),
#     ([])
#   ])
#   @mock.patch("src.utils.daos.dao.DAO._get_column_names", autospec=True)
#   def test_control_keys_pass(self, mockedGCN, sut, keys):
#     """Test that control keys raises exception."""
#     mockedGCN.return_value = ["topic", "name", "body"]
#     result = sut._control_keys(keys)

#     assert result == None

#   @mock.patch("src.utils.daos.dao.DAO._connect_get_cursor", autospec=True)
#   def test_get_column_names(self, mockedCGC, sut):
#     """Get column names."""
#     faked_columns = [(0, "id", None), (1, "username", None), (2, "role", None)]

#     mocked_cursor = mock.MagicMock()
#     mocked_cursor.fetchall.return_value = faked_columns
#     mockedCGC.return_value = mocked_cursor

#     result = sut._get_column_names()

#     assert result == ["id", "username", "role"]

#   @mock.patch("src.utils.daos.dao.DAO._connect_get_cursor", autospec=True)
#   def test_get_column_names_exception(self, mockedCGC, sut):
#     """Get column names."""
#     faked_columns = None

#     mocked_cursor = mock.MagicMock()
#     mocked_cursor.fetchall.return_value = faked_columns
#     mockedCGC.return_value = mocked_cursor

#     with pytest.raises(Exception):
#       sut._get_column_names()

# @pytest.mark.integration
# class TestIntegrationDAO:
#   """Integration tests."""

#   @pytest.mark.parametrize("table_name, id, expected",[
#     ("user", 1, "admin"),
#     ("user", 5, "johndoe")
#   ])
#   def test_get_one(self, sut_int, id, expected):
#     """Test get one user."""
#     data = sut_int.get_one(id)
    
#     assert data["username"] == expected

#   @pytest.mark.parametrize("table_name", ["user"])
#   def test_get_one_none(self, sut_int):
#     """Test when no match in database for one user."""
#     data = sut_int.get_one(2)

#     assert data is None

#   @pytest.mark.parametrize("table_name", ["user"])
#   def test_create(self, sut_int):
#     """Test to create a user."""
#     input_data = {"username": "tony the tiger"}
#     data = sut_int.create(input_data)

#     assert "id" in data and input_data.items() <= data.items()

#   @pytest.mark.parametrize("table_name, input_data",[
#     ("user", {"username": "admin"}),
#     ("user", {"id": 4, "username": "new_one"}),
#     ("user", {"DROP TABLE user;": True})
#   ])
#   def test_create_fail(self, sut_int, input_data):
#     """Test to create a user with wrong input."""
#     with pytest.raises(Exception):
#       sut_int.create(input_data)

#   @pytest.mark.parametrize("table_name, id, input_data, expected",[
#     ("user", 5, {"username": "tony the tiger"}, True),
#     ("user", 2, {"username": "tony the tiger"}, False),
#   ])
#   def test_update(self, sut_int, id, input_data, expected):
#     """Test return value when updating a user."""
#     result = sut_int.update(id, input_data)

#     assert result == expected

#   @pytest.mark.parametrize("table_name, id, input_data, expected",[
#     ("user", 5, {"username": "tony the tiger"}, "tony the tiger"),
#   ])
#   def test_update_data(self, sut_int, id, input_data, expected):
#     """Test data when updating a user."""
#     result = sut_int.update(id, input_data)

#     conn = sqlite3.connect(test_db)
#     cur = conn.cursor()
#     cur.execute("SELECT username from user where id = ?", (id, ))
#     result = cur.fetchone()

#     conn.close()

#     assert result[0] == expected

#   @pytest.mark.parametrize("table_name, id, expected",[
#     ("post", 1, True),
#     ("post", 200, False),
#   ])
#   def test_delete(self, sut_int, id, expected):
#     """Test return value when updating a user."""
#     result = sut_int.delete(id)

#     assert result == expected

#   @pytest.mark.parametrize("table_name, id",[
#     ("post", 1),
#   ])
#   def test_delete_data(self, sut_int, id):
#     """Test data when updating a user."""
#     result = sut_int.delete(id)

#     conn = sqlite3.connect(test_db)
#     cur = conn.cursor()
#     cur.execute("SELECT deleted from post where id = ?", (id, ))
#     result = cur.fetchone()

#     conn.close()

#     assert re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", result[0])
