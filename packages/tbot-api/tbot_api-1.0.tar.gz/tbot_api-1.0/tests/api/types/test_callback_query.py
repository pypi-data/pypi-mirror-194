from tbot_api.methods import AnswerCallbackQuery
from tbot_api.types import CallbackQuery, User


class TestCallbackQuery:
    def test_answer_alias(self) -> None:
        callback_query = CallbackQuery(
            id="id", from_user=User(id=42, is_bot=False, first_name="name"), chat_instance="chat"
        )
        kwargs = {"text": "foo", "show_alert": True, "url": "https://foo.bar/", "cache_time": 123}

        api_method = callback_query.answer(**kwargs)

        assert isinstance(api_method, AnswerCallbackQuery)
        assert api_method.callback_query_id == callback_query.id

        for key, value in kwargs.items():
            assert getattr(api_method, key) == value
