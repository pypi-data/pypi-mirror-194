from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import InlineKeyboardMarkup, Message
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class SendGame(TelegramMethod[Message]):
    __returns__ = Message

    chat_id: int
    game_short_name: str
    message_thread_id: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_to_message_id: Optional[int] = None
    allow_sending_without_reply: Optional[bool] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="sendGame", data=data)
