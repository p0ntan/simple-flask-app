import pytest
import unittest.mock as mock
from src.utils.dao import DAO

faked_rows = ((1, "johndoe", "author"), (2, "admin", "admin"), (3, "elmapelma", "moderator"))
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
class TestDAO:
  @pytest.mark.parametrize("rows, names, expected", [
    (faked_rows,(("id",), ("username", ), ("role", )), faked_expected),
    ([], (("id",), ("username", ), ("role", )), [])
  ])
  @mock.patch("src.utils.dao.DAO._connect_get_cursor", autospec=True)
  @mock.patch("src.utils.dao.DAO._disconnect", autospec=True)
  def test_get_all(self, mockedDisconnect, mockedCGC, sut, rows, names, expected):
    mocked_cursor = mock.MagicMock()
    mocked_cursor.execute.return_value = rows
    mocked_cursor.description = names

    mockedCGC.return_value = mocked_cursor
    mockedDisconnect.side_effect = None

    result = sut.get_all()

    assert result == expected

  @mock.patch("src.utils.dao.DAO._connect_get_cursor", autospec=True)
  def test_get_all_exception(self, mockedCGC, sut):
    mocked_cursor = mock.MagicMock()
    mocked_cursor.execute.side_effect = Exception
    mockedCGC.return_value = mocked_cursor

    with pytest.raises(Exception):
      sut.get_all()
