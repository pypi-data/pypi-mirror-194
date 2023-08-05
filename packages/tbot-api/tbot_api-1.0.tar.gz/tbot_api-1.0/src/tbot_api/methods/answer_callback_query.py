from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class AnswerCallbackQuery(TelegramMethod[bool]):
    __returns__ = bool

    callback_query_id: str
    text: Optional[str] = None
    show_alert: Optional[bool] = None
    url: Optional[str] = None
    cache_time: Optional[int] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="answerCallbackQuery", data=data)
