import pytest
import unittest.mock as mock
from src.models.topic import Topic
from src.static.types import TopicData
from src.errors.customerrors import UnauthorizedException, NoDataException


@pytest.fixture
def sut():
    """SUT for unittest."""
    user = mock.MagicMock()
    user.id = 1
    user.to_dict.return_value = {"user_id": 1}
    topic_data: TopicData = {
        "topic_id": 12,
        "title": "Test title",
        "category": 1,
        "created": "2020-01-01",
        "disabled": False,
    }

    return Topic(user, topic_data)


@pytest.mark.models
@pytest.mark.unit
class TestUnitTopic:
    """Unit test for topic model."""

    def test_init_topic_missing_keys(self):
        """Test init topic without required keys."""
        topic_data: TopicData = {"title": "keys missing"}  # type: ignore
        user = mock.MagicMock()

        with pytest.raises(KeyError):
            Topic(user, topic_data)

    @mock.patch("src.models.topic.Topic.editor_has_permission")
    def test_update_with_access(self, mocked_ehp, sut):
        """Test update method, only updating avalible attributes even when trying for others."""
        new_title = "new title"
        topic_data = {"title": new_title, "topic_id": 24}
        editor = mock.MagicMock()
        mocked_ehp.return_value = True

        new_data = sut.update(topic_data, editor)

        assert new_data == {"title": new_title} and sut._topic_id == 12

    @mock.patch("src.models.topic.Topic.editor_has_permission")
    def test_update_no_access(self, mocked_ehp, sut):
        """Test update method when trying for user withour right permission."""
        new_title = "new title"
        topic_data = {"title": new_title}
        editor = mock.MagicMock()
        mocked_ehp.return_value = False

        with pytest.raises(UnauthorizedException):
            sut.update(topic_data, editor)

    @pytest.mark.parametrize(
        "id, action, expected, permission",
        [
            (1, "update", True, False),
            (2, "update", False, False),
            (2, "update", True, True),
            (1, "", False, True),
        ],
    )
    def test_has_permission(self, sut, id, action, expected, permission):
        """Test has_permission method."""
        editor = mock.MagicMock()
        editor.id = id
        editor.permission.edit_topic.return_value = permission

        assert sut.editor_has_permission(editor, action) == expected

    @pytest.mark.parametrize(
        "id, action, expected, permission",
        [
            (1, "delete", True, False),
            (2, "delete", False, False),
            (2, "delete", True, True),
            (1, "", False, True),
        ],
    )
    def test_has_delete_permission(self, sut, id, action, expected, permission):
        """Test has_permission method."""
        editor = mock.MagicMock()
        editor.id = id
        editor.permission.delete_topic.return_value = permission

        assert sut.editor_has_permission(editor, action) == expected

    def test_to_dict(self, sut):
        """Test to_dict method."""
        assert sut.to_dict() == {
            "topic_id": 12,
            "created_by": {"user_id": 1},
            "title": "Test title",
            "category": 1,
            "created": "2020-01-01",
            "disabled": False,
            "last_edited": None,
            "deleted": None,
        }

    @mock.patch("src.models.topic.User", autospec=True)
    def test_from_db_by_id(self, mocked_user):
        """Test from_db_by_id method."""
        topic_data = {
            "topic_id": 12,
            "title": "Test title",
            "category": 1,
            "created": "2020-01-01",
            "disabled": False,
            "created_by": {"user_id": 1},
            "deleted": None,
            "last_edited": None,
        }

        mocked_topic_dao = mock.MagicMock()
        mocked_topic_dao.get_one.return_value = topic_data.copy()
        mocked_user_instance = mocked_user.return_value
        mocked_user_instance.to_dict.return_value = {"user_id": 1}

        topic = Topic.from_db_by_id(12, mocked_topic_dao)
        assert topic.to_dict() == topic_data

    @pytest.mark.parametrize(
        "returned, expeced_error", [(None, NoDataException), (Exception, Exception)]
    )
    def test_from_db_by_id_error(self, returned, expeced_error):
        """Test from_db_by_id method but no user found or dao error."""
        mocked_topic_dao = mock.MagicMock()
        mocked_topic_dao.get_one.return_value = returned

        with pytest.raises(expeced_error):
            Topic.from_db_by_id(12, mocked_topic_dao)
