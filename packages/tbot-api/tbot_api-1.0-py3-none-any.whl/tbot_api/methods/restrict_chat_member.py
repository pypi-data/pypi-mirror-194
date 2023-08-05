from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import ChatPermissions
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class RestrictChatMember(TelegramMethod[bool]):
    __returns__ = bool

    chat_id: Union[int, str]
    user_id: int
    permissions: ChatPermissions
    until_date: Optional[Union[int, datetime, timedelta]] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="restrictChatMember", data=data)
