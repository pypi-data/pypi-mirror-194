from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class Close(TelegramMethod[bool]):
    __returns__ = bool

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="close", data=data)
