from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import MenuButtonCommands, MenuButtonDefault, MenuButtonWebApp
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetChatMenuButton(
    TelegramMethod[Union[MenuButtonDefault, MenuButtonWebApp, MenuButtonCommands]]
):
    __returns__ = Union[MenuButtonDefault, MenuButtonWebApp, MenuButtonCommands]

    chat_id: Optional[int] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getChatMenuButton", data=data)
