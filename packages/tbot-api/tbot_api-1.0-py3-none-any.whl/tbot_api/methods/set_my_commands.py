from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import BotCommand, BotCommandScope
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class SetMyCommands(TelegramMethod[bool]):
    __returns__ = bool

    commands: List[BotCommand]
    scope: Optional[BotCommandScope] = None
    language_code: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="setMyCommands", data=data)
