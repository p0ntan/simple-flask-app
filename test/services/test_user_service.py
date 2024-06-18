import os
import pytest
import sqlite3
import unittest.mock as mock
from src.services import UserService
from src.utils.daos import UserDAO
from src.errors.customerrors import NoDataException, UnauthorizedException

base_dir = os.path.dirname(__file__)
test_db = os.getenv("TEST_SQLITE_PATH", "")

johndoe_user = {
    "user_id": 5,
    "username": "johndoe",
    "role": "author",
    "signature": None,
    "avatar": None,
}

admin_user = {
    "user_id": 1,
    "username": "admin",
    "role": "admin",
    "signature": None,
    "avatar": None,
}


@pytest.fixture
def sut():
    """Setup UserService for integrationtest and fucntion-test"""
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

    with mock.patch("src.utils.daos.basedao.get_config") as mocked_config:
        config = mock.MagicMock()
        config.DB_PATH = test_db
        mocked_config.return_value = config
        user_dao = UserDAO("user")
        sut = UserService(user_dao)
        yield sut
        os.remove(test_db)


@pytest.mark.integration
class TestIntegrationUserService:
    """Integration tests"""

    def test_get_by_id(self, sut):
        """Test get user by id"""
        user = sut.get_by_id(5)

        assert user == johndoe_user

    def test_get_by_id_no_user(self, sut):
        """Test get user by id that dosen't exist"""
        with pytest.raises(NoDataException):
            sut.get_by_id(10)

    def test_login(self, sut):
        """Test login a user by username"""
        user = sut.login("johndoe", "password")

        assert user == johndoe_user

    def test_login_no_user(self, sut):
        """Test login user that dosen't exist"""
        with pytest.raises(NoDataException):
            sut.login("no_user", "password")

    def test_create(self, sut):
        """Test create a user. Only username should be used even with more keys in data."""
        user = sut.create(
            {
                "username": "sven",
                "role": "what I want",  # Should not work, role should be author by default.
            }
        )

        assert user["username"] == "sven" and user["role"] == "author"

    def test_create_errors(self, sut):
        """Test create a user that already exists."""
        with pytest.raises(Exception):
            sut.create({"username": "admin"})


@pytest.mark.scenario
class TestScenarioUserService:
    """Scenario tests"""

    @pytest.mark.parametrize(
        "user_id, new_data, editor_data, expected_data",
        [
            (
                5,
                {"signature": "this is a new sign", "role": "moderator"},
                johndoe_user,
                ["this is a new sign", "author"],
            ),
            (
                5,
                {"signature": "this is a new sign, set by admin", "role": "moderator"},
                admin_user,
                ["this is a new sign, set by admin", "moderator"],
            ),
        ],
    )
    def test_update(self, sut, user_id, new_data, editor_data, expected_data):
        """Test updating a user."""
        result = sut.update(user_id=user_id, new_data=new_data, editor_data=editor_data)

        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        raw = cursor.execute(
            "SELECT signature, role from user where id = ?", (user_id,)
        )
        data = raw.fetchone()
        conn.close()

        assert (
            result == True
            and data[0] == expected_data[0]
            and data[1] == expected_data[1]
        )

    @pytest.mark.parametrize(
        "user_id, expected_error", [(2, NoDataException), (3, UnauthorizedException)]
    )
    def test_update_exceptions(self, sut, user_id, expected_error):
        """Test update with wrong users."""
        new_data = {"signature": "new sign"}

        with pytest.raises(expected_error):
            sut.update(user_id=user_id, new_data=new_data, editor_data=johndoe_user)

    def test_delete(self, sut):
        """Test deleteing a user."""
        user_id = 5
        result = sut.delete(user_id=user_id, editor_data=johndoe_user)

        # conn = sqlite3.connect(test_db)
        # cursor = conn.cursor()
        # raw = cursor.execute("SELECT signature from user where id = ?", (user_id, ))
        # data = raw.fetchone()
        # conn.close()

        assert result == True

    def test_delete_exceptions(self, sut):
        """Test delete with wrong user."""
        with pytest.raises(UnauthorizedException):
            sut.delete(user_id=3, editor_data=johndoe_user)
