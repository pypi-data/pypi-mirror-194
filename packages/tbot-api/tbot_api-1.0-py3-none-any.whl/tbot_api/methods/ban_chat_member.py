from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class BanChatMember(TelegramMethod[bool]):
    __returns__ = bool

    chat_id: Union[int, str]
    user_id: int
    until_date: Optional[Union[int, datetime, timedelta]] = None
    revoke_messages: Optional[bool] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="banChatMember", data=data)
