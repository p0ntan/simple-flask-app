import pytest
import unittest.mock as mock
from src.models.user import User
from src.static.types import UserData
from src.errors.customerrors import NoDataException, UnauthorizedException


@pytest.fixture
def sut():
    """SUT for unittest."""
    topic_data: UserData = {"user_id": 666, "username": "test", "role": "admin"}

    return User(topic_data)


@pytest.mark.models
@pytest.mark.unit
class TestUnitUser:
    """Unit test for user model."""

    def test_init_user_missing_keys(self):
        """Test init user without required keys."""
        user_data: UserData = {"role": "admin"}  # type: ignore

        with pytest.raises(KeyError):
            User(user_data)

    @pytest.mark.parametrize(
        "new_data, expected_return, user_id",
        (
            [
                (
                    {"signature": "new sign", "avatar": "new avatar", "user_id": 24},
                    {"signature": "new sign", "avatar": "new avatar"},
                    666,
                ),
                ({}, {"signature": None, "avatar": None}, 666),
            ]
        ),
    )
    @mock.patch("src.models.user.User.editor_has_permission")
    def test_update_with_access(
        self, mocked_ehp, sut, new_data, expected_return, user_id
    ):
        """Test update method, only updating avalible attributes even when trying for others."""
        editor = mock.MagicMock()
        mocked_ehp.return_value = True

        result = sut.update(new_data, editor)

        assert result == expected_return and sut._user_id == user_id

    @mock.patch("src.models.user.User.editor_has_permission")
    def test_update_no_access(self, mocked_ehp, sut):
        """Test update method when trying for user withour right permission."""
        new_data = {"signature": "new sign"}
        editor = mock.MagicMock()
        mocked_ehp.return_value = False

        with pytest.raises(UnauthorizedException):
            sut.update(new_data, editor)

    @pytest.mark.parametrize("id, action, expected, permission", [
        (666, "update", True, False),
        (2, "update", False, False),
        (2, "update", True, True),
        (666, "", False, True)
        ])
    def test_has_permission(self, sut, id, action, expected, permission):
        """Test has_permission method."""
        editor = mock.MagicMock()
        editor.id = id
        editor.permission.edit_user.return_value = permission

        assert sut.editor_has_permission(editor, action) == expected

    @pytest.mark.parametrize("id, action, expected, permission", [
        (666, "delete", True, False),
        (2, "delete", False, False),
        (2, "delete", True, True),
        (666, "", False, True)
        ])
    def test_has_delete_permission(self, sut, id, action, expected, permission):
        """Test has_permission method."""
        editor = mock.MagicMock()
        editor.id = id
        editor.permission.delete_user.return_value = permission

        assert sut.editor_has_permission(editor, action) == expected

    def test_to_dict(self, sut):
        """Test to_dict method."""
        assert sut.to_dict() == {
            "user_id": 666,
            "username": "test",
            "role": "admin",
            "signature": None,
            "avatar": None,
        }

    @mock.patch("src.models.post.User", autospec=True)
    def test_from_db_by_id(self, mocked_user):
        """Test from_db_by_id method."""
        user_data = {
            "user_id": 666,
            "username": "test",
            "role": "admin",
            "signature": "has signature",
            "avatar": None,
        }

        mocked_user_dao = mock.MagicMock()
        mocked_user_dao.get_one.return_value = user_data
        user = User.from_db_by_id(12, mocked_user_dao)
        assert user.to_dict() == user_data

    @pytest.mark.parametrize(
        "returned, expeced_error", [(None, NoDataException), (Exception, Exception)]
    )
    def test_from_db_by_id_error(self, returned, expeced_error):
        """Test from_db_by_id method but no user found or dao error."""
        mocked_user_dao = mock.MagicMock()
        mocked_user_dao.get_one.return_value = returned

        with pytest.raises(expeced_error):
            User.from_db_by_id(12, mocked_user_dao)
