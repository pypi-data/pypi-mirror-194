from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import BotCommandScope
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class DeleteMyCommands(TelegramMethod[bool]):
    __returns__ = bool

    scope: Optional[BotCommandScope] = None
    language_code: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="deleteMyCommands", data=data)
