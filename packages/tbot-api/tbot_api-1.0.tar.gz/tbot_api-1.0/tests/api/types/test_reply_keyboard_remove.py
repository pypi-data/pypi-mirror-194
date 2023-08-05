import pytest

from tbot_api.types import ReplyKeyboardRemove


class TestReplyKeyboardRemove:
    def test_remove_keyboard_default_is_true(self) -> None:
        assert (
            ReplyKeyboardRemove.__fields__["remove_keyboard"].default is True
        ), "Remove keyboard has incorrect default value!"

    @pytest.mark.parametrize(
        "kwargs,expected",
        [({}, True), ({"remove_keyboard": True}, True)],
    )
    def test_remove_keyboard_values(self, kwargs, expected) -> None:
        assert ReplyKeyboardRemove(**kwargs).remove_keyboard is expected
