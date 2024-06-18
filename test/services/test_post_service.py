import os
import re
import pytest
import sqlite3
import unittest.mock as mock
from src.services import PostService
from src.utils.daos import UserDAO, PostDAO
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

moderator = {
    "user_id": 3,
    "username": "moderator",
    "role": "moderator",
    "signature": None,
    "avatar": None,
}


@pytest.fixture
def sut():
    """Setup Postservice for integrationtest and scenario-test"""
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
        post_dao = PostDAO("post")
        sut = PostService(post_dao, user_dao)
        yield sut
        os.remove(test_db)


@pytest.mark.integration
class TestIntegrationPostService:
    """Integration tests"""

    def test_get_by_id(self, sut):
        """Test get post by id"""
        post = sut.get_by_id(1)

        assert post["post_id"] == 1 and post["body"] == "Has no title"

    @pytest.mark.parametrize("post_id", [(244), (3)])
    def test_get_by_id_no_post(self, sut, post_id):
        """Test get post by id that dosen't exist or is deleted."""
        with pytest.raises(NoDataException):
            sut.get_by_id(post_id)

    def test_create(self, sut):
        """Test create a post."""
        post = sut.create(
            {
                "topic_id": 4,
                "body": "Body for test",
            },
            johndoe_user,
        )

        assert (
            post["topic_id"] == 4
            and post["body"] == "Body for test"
            and post["author"] == johndoe_user
        )

    def test_create_errors(self, sut):
        """Test create a topic with missing data."""
        with pytest.raises(Exception):
            sut.create(
                {
                    "topic_id": 4,
                    # "body": "missing"
                },
                johndoe_user,
            )


@pytest.mark.scenario
class TestScenarioUserService:
    """Scenario tests"""

    @pytest.mark.parametrize(
        "editor_data",
        [(johndoe_user), (admin_user), (moderator)],
    )
    def test_update(self, sut, editor_data):
        """Test updating a post."""
        post_id = 1
        new_title = "new title"
        new_body = "this is a new body"
        new_data = {"title": new_title, "body": new_body}

        result = sut.update(1, new_data, editor_data=editor_data)

        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        raw = cursor.execute("SELECT title, body from post where id = ?", (post_id,))
        data = raw.fetchone()
        conn.close()

        assert result == True and data[0] == new_title and data[1] == new_body

    @pytest.mark.parametrize(
        "post_id, editor_data, expected_error",
        [
            (2, johndoe_user, UnauthorizedException),
            (3, admin_user, NoDataException),  # Deleted post
            (244, admin_user, NoDataException),  # Post dosen't exist
        ],
    )
    def test_update_exceptions(self, sut, post_id, editor_data, expected_error):
        """Test update post with unautharized users or that post down't exists."""
        new_data = {"signature": "new sign"}

        with pytest.raises(expected_error):
            sut.update(post_id, new_data, editor_data)

    @pytest.mark.parametrize(
        "post_id, editor_data", [(8, johndoe_user), (8, admin_user)]
    )
    def test_delete(self, sut, post_id, editor_data):
        """Test deleteing a post."""
        result = sut.delete(post_id, editor_data)

        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        raw = cursor.execute("SELECT deleted from post where id = ?", (post_id,))
        data = raw.fetchone()
        conn.close()

        assert result == True and re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", data[0])

    @pytest.mark.parametrize(
        "post_id, editor_data", [(8, moderator), (2, johndoe_user)]
    )
    def test_delete_exceptions(self, sut, post_id, editor_data):
        """Test delete post with unauthorized user."""
        with pytest.raises(UnauthorizedException):
            sut.delete(post_id, editor_data)
