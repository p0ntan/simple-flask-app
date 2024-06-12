import pytest
from src.models.user import User
from src.static.types import UserData

@pytest.mark.models
@pytest.mark.unit
class TestUnitUser:
  """Unit test for user model."""

  def test_init_user_missing_keys(self):
    """Test init user without required keys."""
    user_data: UserData = {"role": "admin"} # type: ignore

    with pytest.raises(KeyError):
      User(user_data)

  def test_user_to_dict(self):
    """Test if to_dict returns a dictionary with the correct data."""
    input_data = {"user_id": 1, "username": "test", "role": "admin"}
    user_data = UserData(**input_data)

    user = User(user_data)
    user_dict = user.to_dict()

    assert user_data.items() <= user_dict.items()
    assert "avatar" in user_dict and "signature" in user_dict

  def test_update_user(self):
    """Test if update updates the user correctly."""
    input_data = {"user_id": 1, "username": "test", "role": "admin"}
    user_data = UserData(**input_data)
    user = User(user_data)

    new_data  = {"username": "updated_test", "role": "author"}
    user.update(new_data)

    result: UserData = user.to_dict()

    assert result["username"] == "updated_test" and result["role"] == "author"
