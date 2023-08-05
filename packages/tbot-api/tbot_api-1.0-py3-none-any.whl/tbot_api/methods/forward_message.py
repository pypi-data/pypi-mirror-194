from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import Message
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class ForwardMessage(TelegramMethod[Message]):
    __returns__ = Message

    chat_id: Union[int, str]
    from_chat_id: Union[int, str]
    message_id: int
    message_thread_id: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="forwardMessage", data=data)
