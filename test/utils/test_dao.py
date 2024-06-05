import pytest
import unittest.mock as mock
from src.utils.dao import DAO
from src.errors.customerrors import KeyUnmutableException

faked_rows = ((1, "johndoe", "author"), (2, "admin", "admin"), (3, "elmapelma", "moderator"))
faked_names = (("id",), ("username", ), ("role", ))
faked_expected = [
  {
    "id": 1,
    "username": "johndoe",
    "role": "author"
  },
  {
    "id": 2,
    "username": "admin",
    "role": "admin"
  },
  {
    "id": 3,
    "username": "elmapelma",
    "role": "moderator"
  },
]

@pytest.fixture
def sut():
  sut = DAO("")

  return sut


@pytest.mark.unit
class TestUnitDAO:
  @pytest.mark.parametrize("result, names, expected", [
    ((2, "admin", "admin"),faked_names, {
      "id": 2,
      "username": "admin",
      "role": "admin"
    }),
    (None, faked_names, None)
  ])
  @mock.patch("src.utils.dao.DAO._connect_get_cursor", autospec=True)
  @mock.patch("src.utils.dao.DAO._disconnect", autospec=True)
  def test_get_one(self, mockedDisconnect, mockedCGC, sut, result, names, expected):
    """
    Get one
    """
    mocked_cursor = mock.MagicMock()
    mocked_cursor.execute.side_effect = None
    mocked_cursor.description = names
    mocked_cursor.fetchone.return_value = result

    mockedCGC.return_value = mocked_cursor
    mockedDisconnect.side_effect = None

    result = sut.get_one(2)

    assert result == expected

  @mock.patch("src.utils.dao.DAO._connect_get_cursor", autospec=True)
  def test_get_one_exception(self, mockedCGC, sut):
    """
    Get one - exception
    """
    mocked_cursor = mock.MagicMock()
    mocked_cursor.execute.side_effect = None
    mocked_cursor.fetchone.side_effect = Exception
    mockedCGC.return_value = mocked_cursor

    with pytest.raises(Exception):
      sut.get_one(2)

  @pytest.mark.parametrize("rows, names, expected", [
    (faked_rows,(("id",), ("username", ), ("role", )), faked_expected),
    ([], (("id",), ("username", ), ("role", )), [])
  ])
  @mock.patch("src.utils.dao.DAO._connect_get_cursor", autospec=True)
  @mock.patch("src.utils.dao.DAO._disconnect", autospec=True)
  def test_get_all(self, mockedDisconnect, mockedCGC, sut, rows, names, expected):
    """
    Get all
    """
    mocked_cursor = mock.MagicMock()
    mocked_cursor.execute.return_value = rows
    mocked_cursor.description = names

    mockedCGC.return_value = mocked_cursor
    mockedDisconnect.side_effect = None

    result = sut.get_all()

    assert result == expected

  @mock.patch("src.utils.dao.DAO._connect_get_cursor", autospec=True)
  def test_get_all_exception(self, mockedCGC, sut):
    """
    Get all - exception
    """
    mocked_cursor = mock.MagicMock()
    mocked_cursor.execute.side_effect = Exception
    mockedCGC.return_value = mocked_cursor

    with pytest.raises(Exception):
      sut.get_all()

  @mock.patch("src.utils.dao.DAO._control_keys", autospec=True)
  @mock.patch("src.utils.dao.DAO._disconnect", autospec=True)
  def test_update_exception(self, mocked_DC, mockedCK, sut):
    """Test that when an exception is raised the _disconnect in finally block is called."""
    mockedCK.side_effect = KeyUnmutableException("Key for column not valid.")

    with pytest.raises(KeyUnmutableException):
      sut.update(2, {})
    mocked_DC.assert_called_once()

  @pytest.mark.parametrize("keys", [
    (["topic", "name", "fail"]),
    (["id"])
  ])
  @mock.patch("src.utils.dao.DAO._get_column_names", autospec=True)
  def test_control_keys_fail(self, mockedGCN, sut, keys):
    """Test that control keys raises exception."""
    mockedGCN.return_value = ["topic", "name", "body"]

    with pytest.raises(KeyUnmutableException):
      sut._control_keys(keys)

  @pytest.mark.parametrize("keys", [
    (["topic", "name", "body"]),
    (["name"]),
    ([])
  ])
  @mock.patch("src.utils.dao.DAO._get_column_names", autospec=True)
  def test_control_keys_pass(self, mockedGCN, sut, keys):
    """Test that control keys raises exception."""
    mockedGCN.return_value = ["topic", "name", "body"]
    result = sut._control_keys(keys)

    assert result == None

  @mock.patch("src.utils.dao.DAO._connect_get_cursor", autospec=True)
  def test_get_column_names(self, mockedCGC, sut):
    """Get column names."""
    faked_columns = [(0, "id", None), (1, "username", None), (2, "role", None)]

    mocked_cursor = mock.MagicMock()
    mocked_cursor.fetchall.return_value = faked_columns
    mockedCGC.return_value = mocked_cursor

    result = sut._get_column_names()

    assert result == ["id", "username", "role"]

  @mock.patch("src.utils.dao.DAO._connect_get_cursor", autospec=True)
  def test_get_column_names_exception(self, mockedCGC, sut):
    """Get column names."""
    faked_columns = None

    mocked_cursor = mock.MagicMock()
    mocked_cursor.fetchall.return_value = faked_columns
    mockedCGC.return_value = mocked_cursor

    with pytest.raises(Exception):
      sut._get_column_names()
