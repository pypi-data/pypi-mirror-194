from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import InlineKeyboardMarkup, Poll
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class StopPoll(TelegramMethod[Poll]):
    __returns__ = Poll

    chat_id: Union[int, str]
    message_id: int
    reply_markup: Optional[InlineKeyboardMarkup] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="stopPoll", data=data)
