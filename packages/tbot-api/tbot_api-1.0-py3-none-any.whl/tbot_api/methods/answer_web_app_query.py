from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..types import InlineQueryResult, SentWebAppMessage
from .base import Request, TelegramMethod, prepare_parse_mode

if TYPE_CHECKING:
    from ..bot import Bot


class AnswerWebAppQuery(TelegramMethod[SentWebAppMessage]):
    __returns__ = SentWebAppMessage

    web_app_query_id: str
    result: InlineQueryResult

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        prepare_parse_mode(
            bot, data["result"], parse_mode_property="parse_mode", entities_property="entities"
        )

        return Request(method="answerWebAppQuery", data=data)
