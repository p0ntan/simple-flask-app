import os
import pytest
import sqlite3
import unittest.mock as mock
from src.utils.daos import UserDAO

base_dir = os.path.dirname(__file__)
test_db = os.path.join(base_dir, "test_data/test_db.sqlite")
faked_rows = (
    (1, "johndoe", "author"),
    (2, "admin", "admin"),
    (3, "elmapelma", "moderator"),
)
faked_names = (("id",), ("username",), ("role",))
faked_expected = [
    {"id": 1, "username": "johndoe", "role": "author"},
    {"id": 2, "username": "admin", "role": "admin"},
    {"id": 3, "username": "elmapelma", "role": "moderator"},
]


@pytest.fixture
def sut_int():
    """SUT for integrationtest."""
    test_data = os.path.join(base_dir, "test_data/insert.sql")
    files = ["./db/ddl.sql", test_data]

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    for file in files:
        with open(file, "r") as f:
            sql_commands = f.read()
            cursor.executescript(sql_commands)

    conn.commit()
    conn.close()

    with mock.patch("src.utils.daos.basedao.os.environ.get") as db_path:
        db_path.return_value = test_db
        sut = UserDAO("user")
        yield sut
        os.remove(test_db)


@pytest.fixture
def sut():
    """SUT for unittest."""
    sut = UserDAO("user")

    return sut


@pytest.mark.unit
class TestUnitDAO:
    @pytest.mark.parametrize(
        "result, expected",
        [
            (
                {"id": 2, "username": "admin", "role": "admin"},
                {"id": 2, "username": "admin", "role": "admin"},
            ),
            (None, None),
        ],
    )
    @mock.patch("src.utils.daos.UserDAO._get_connection", autospec=True)
    @mock.patch("src.utils.daos.UserDAO._disconnect", autospec=True)
    def test_get_one(self, mockedDisconnect, mockedGetConnection, sut, result, expected):
        """
        Get one
        """
        mocked_execute = mock.MagicMock()
        mocked_execute.fetchone.return_value = result
        mocked_connection = mock.MagicMock()
        mocked_connection.execute.return_value = mocked_execute
        mockedGetConnection.return_value = mocked_connection
        mockedDisconnect.side_effect = None

        result = sut.get_one(2)

        assert result == expected

    @mock.patch("src.utils.daos.UserDAO._get_connection", autospec=True)
    def test_get_one_exception(self, mockedGetConnection, sut):
        """
        Get one - exception
        """
        mocked_connection = mock.MagicMock()
        mocked_connection.execute.side_effect = Exception
        mockedGetConnection.return_value = mocked_connection

        with pytest.raises(Exception):
            sut.get_one(2)

    @mock.patch("src.utils.daos.UserDAO._get_connection", autospec=True)
    @mock.patch("src.utils.daos.UserDAO._disconnect", autospec=True)
    def test_update_exception(self, mockedDisconnect, mockedGetConnection, sut):
        """Test when an exception is raised due to wrong input, conn.close in finally block is called."""
        connection = mock.MagicMock()
        mockedGetConnection.return_value = connection

        with pytest.raises(Exception):
            sut.update(2, {})

        mockedDisconnect.assert_called_once()

    @mock.patch("src.utils.daos.UserDAO._get_connection", autospec=True)
    @mock.patch("src.utils.daos.UserDAO._disconnect", autospec=True)
    def test_delete_exception(self, mockedDisconnect, mockedGetConnection, sut):
        """Test that when an exception is raised the _disconnect in finally block is called."""
        connection = mock.MagicMock()
        mockedGetConnection.return_value = connection

        with pytest.raises(Exception):
            sut.delete(2)

        mockedDisconnect.assert_called_once()

@pytest.mark.integration
class TestIntegrationUserDAO:
    """Integration tests."""

    @pytest.mark.parametrize("id, expected", [(1, "admin"), (5, "johndoe")])
    def test_get_one(self, sut_int, id, expected):
        """Test get one user."""
        data = sut_int.get_one(id)

        assert data["username"] == expected

    def test_get_one_none(self, sut_int):
        """Test when no match in database for one user."""
        data = sut_int.get_one(2)

        assert data is None

    def test_create(self, sut_int):
        """Test to create a user."""
        input_data = {"username": "tony the tiger"}
        data = sut_int.create(input_data)

        assert "user_id" in data and input_data.items() <= data.items()

    @pytest.mark.parametrize(
        "input_data", [({"username": "admin"}), ({"DROP TABLE user;": True})]
    )
    def test_create_fail(self, sut_int, input_data):
        """Test to create a user with wrong input."""
        with pytest.raises(Exception):
            sut_int.create(input_data)

    @pytest.mark.parametrize(
        "id, input_data, expected",
        [
            (5, {"username": "tony the tiger"}, True),
            (2, {"username": "tony the tiger"}, False),
        ],
    )
    def test_update(self, sut_int, id, input_data, expected):
        """Test return value when updating a user."""
        result = sut_int.update(id, input_data)

        assert result == expected

    @pytest.mark.parametrize(
        "id, input_data, expected",
        [
            (5, {"username": "tony the tiger"}, "tony the tiger"),
        ],
    )
    def test_update_data(self, sut_int, id, input_data, expected):
        """Test data when updating a user."""
        result = sut_int.update(id, input_data)

        conn = sqlite3.connect(test_db)
        cur = conn.cursor()
        cur.execute("SELECT username from user where id = ?", (id,))
        result = cur.fetchone()

        conn.close()

        assert result[0] == expected

    @pytest.mark.parametrize(
        "user_name, expected_user_type",
        [
            ("admin", dict),
            ("nonexistent_user", type(None)),
        ],
    )
    def test_get_user_by_name_type(self, sut_int, user_name, expected_user_type):
        """Test that get_user_by_name returns the correct type."""
        user = sut_int.get_user_by_username(user_name)

        assert isinstance(user, expected_user_type)

    @pytest.mark.parametrize(
        "username, expected_user",
        [
            (
                "admin",
                {
                    "user_id": 1,
                    "username": "admin",
                    "role": "admin",
                    "signature": None,
                    "avatar": None,
                },
            ),
            (
                "johndoe",
                {
                    "user_id": 5,
                    "username": "johndoe",
                    "role": "author",
                    "signature": None,
                    "avatar": None,
                },
            ),
        ],
    )
    def test_get_user_by_username(self, sut_int, username, expected_user):
        """Test to get user by username by controlling data."""
        user = sut_int.get_user_by_username(username)

        assert user == expected_user
