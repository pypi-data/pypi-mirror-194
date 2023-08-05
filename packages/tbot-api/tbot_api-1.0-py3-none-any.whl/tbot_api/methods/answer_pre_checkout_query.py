from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class AnswerPreCheckoutQuery(TelegramMethod[bool]):
    __returns__ = bool

    pre_checkout_query_id: str
    ok: bool
    error_message: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="answerPreCheckoutQuery", data=data)
