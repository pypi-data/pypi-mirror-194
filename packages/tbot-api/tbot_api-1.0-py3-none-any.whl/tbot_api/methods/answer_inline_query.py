from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import InlineQueryResult
from .base import Request, TelegramMethod, prepare_parse_mode

if TYPE_CHECKING:
    from ..bot import Bot


class AnswerInlineQuery(TelegramMethod[bool]):
    __returns__ = bool

    inline_query_id: str
    results: List[InlineQueryResult]
    cache_time: Optional[int] = None
    is_personal: Optional[bool] = None
    next_offset: Optional[str] = None
    switch_pm_text: Optional[str] = None
    switch_pm_parameter: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        input_message_contents = []
        for result in data["results"]:
            input_message_content = result.get("input_message_content", None)
            if input_message_content is not None:
                input_message_contents.append(input_message_content)

        prepare_parse_mode(bot, data["results"] + input_message_contents)
        return Request(method="answerInlineQuery", data=data)
