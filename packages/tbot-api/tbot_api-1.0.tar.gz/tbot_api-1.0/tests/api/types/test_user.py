from tbot_api.types import User


class TestUser:
    def test_get_profile_photos(self) -> None:
        user = User(id=42, is_bot=False, first_name="Test", last_name="User")

        method = user.get_profile_photos(description="test")
        assert method.user_id == user.id
