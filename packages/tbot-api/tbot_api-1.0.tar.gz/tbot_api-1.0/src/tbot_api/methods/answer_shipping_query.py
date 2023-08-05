from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import ShippingOption
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class AnswerShippingQuery(TelegramMethod[bool]):
    __returns__ = bool

    shipping_query_id: str
    ok: bool
    shipping_options: Optional[List[ShippingOption]] = None
    error_message: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="answerShippingQuery", data=data)
