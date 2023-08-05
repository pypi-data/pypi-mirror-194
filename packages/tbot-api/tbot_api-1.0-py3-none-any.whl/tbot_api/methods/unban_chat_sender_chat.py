from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class UnbanChatSenderChat(TelegramMethod[bool]):
    __returns__ = bool

    chat_id: Union[int, str]
    sender_chat_id: int

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="unbanChatSenderChat", data=data)
