from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class SendChatAction(TelegramMethod[bool]):
    __returns__ = bool

    chat_id: Union[int, str]
    action: str
    message_thread_id: Optional[int] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="sendChatAction", data=data)
