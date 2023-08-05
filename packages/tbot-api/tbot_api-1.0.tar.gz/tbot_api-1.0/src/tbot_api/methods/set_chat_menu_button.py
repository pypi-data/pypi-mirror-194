from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import MenuButtonCommands, MenuButtonDefault, MenuButtonWebApp
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class SetChatMenuButton(TelegramMethod[bool]):
    __returns__ = bool

    chat_id: Optional[int] = None
    menu_button: Optional[Union[MenuButtonDefault, MenuButtonWebApp, MenuButtonCommands]] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="setChatMenuButton", data=data)
