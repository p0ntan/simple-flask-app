import pytest
import unittest.mock as mock
from src.models.post import Post
from src.static.types import PostData
from src.errors.customerrors import UnauthorizedException, NoDataException


@pytest.fixture
def sut():
    """SUT for unittest."""
    user = mock.MagicMock()
    user.id = 1
    user.to_dict.return_value = {"user_id": 1}
    post_data: PostData = {
        "post_id": 12,
        "topic_id": 2,
        "body": "Lorum impsum and such.",
        "created": "2020-01-01",
    }

    return Post(user, post_data)


@pytest.mark.models
@pytest.mark.unit
class TestUnitPost:
    """Unit test for post model."""

    def test_init_post_missing_keys(self):
        """Test init post without required keys."""
        post_data: PostData = {"body": "keys missing"}  # type: ignore
        user = mock.MagicMock()

        with pytest.raises(KeyError):
            Post(user, post_data)

    @pytest.mark.parametrize(
        "new_data, expected_return, topic_id",
        (
            [
                (
                    {"title": "new title", "body": "new body", "topic_id": 24},
                    {"title": "new title", "body": "new body"},
                    2,
                ),
                (
                    {"title": "new title", "topic_id": 24},
                    {"title": "new title", "body": "Lorum impsum and such."},
                    2,
                ),
            ]
        ),
    )
    @mock.patch("src.models.post.Post.editor_has_permission")
    def test_update_with_access(
        self, mocked_ehp, sut, new_data, expected_return, topic_id
    ):
        """Test update method, only updating avalible attributes even when trying for others."""
        editor = mock.MagicMock()
        mocked_ehp.return_value = True

        result = sut.update(new_data, editor)

        assert result == expected_return and sut._topic_id == topic_id

    @mock.patch("src.models.post.Post.editor_has_permission")
    def test_update_no_access(self, mocked_ehp, sut):
        """Test update method when trying for user withour right permission."""
        new_title = "new title"
        topic_data = {"title": new_title}
        editor = mock.MagicMock()
        mocked_ehp.return_value = False

        with pytest.raises(UnauthorizedException):
            sut.update(topic_data, editor)

    @pytest.mark.parametrize("id, expected", [(1, True), (2, False)])
    def test_has_permission(self, sut, id, expected):
        """Test has_permission method."""
        editor = mock.MagicMock()
        editor.id = id

        assert sut.editor_has_permission(editor) == expected

    def test_to_dict(self, sut):
        """Test to_dict method."""
        assert sut.to_dict() == {
            "post_id": 12,
            "topic_id": 2,
            "author": {"user_id": 1},
            "title": None,
            "body": "Lorum impsum and such.",
            "created": "2020-01-01",
            "last_edited": None,
            "deleted": None,
        }

    @mock.patch("src.models.post.User", autospec=True)
    def test_from_db_by_id(self, mocked_user):
        """Test from_db_by_id method."""
        topic_data = {
            "post_id": 12,
            "topic_id": 2,
            "author": {"user_id": 1},
            "title": None,
            "body": "Lorum impsum and such.",
            "created": "2020-01-01",
            "last_edited": None,
            "deleted": None,
        }

        mocked_post_dao = mock.MagicMock()
        mocked_post_dao.get_one.return_value = topic_data.copy()
        mocked_user_instance = mocked_user.return_value
        mocked_user_instance.to_dict.return_value = {"user_id": 1}

        topic = Post.from_db_by_id(12, mocked_post_dao)
        assert topic.to_dict() == topic_data

    @pytest.mark.parametrize(
        "returned, expeced_error", [(None, NoDataException), (Exception, Exception)]
    )
    def test_from_db_by_id_error(self, returned, expeced_error):
        """Test from_db_by_id method but no user found or dao error."""
        mocked_topic_dao = mock.MagicMock()
        mocked_topic_dao.get_one.return_value = returned

        with pytest.raises(expeced_error):
            Post.from_db_by_id(12, mocked_topic_dao)
