from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from ..types import PassportElementError
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class SetPassportDataErrors(TelegramMethod[bool]):
    __returns__ = bool

    user_id: int
    errors: List[PassportElementError]

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="setPassportDataErrors", data=data)
