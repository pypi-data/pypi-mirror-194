from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import ChatInviteLink
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class CreateChatInviteLink(TelegramMethod[ChatInviteLink]):
    __returns__ = ChatInviteLink

    chat_id: Union[int, str]
    name: Optional[str] = None
    expire_date: Optional[Union[datetime.datetime, datetime.timedelta, int]] = None
    member_limit: Optional[int] = None
    creates_join_request: Optional[bool] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="createChatInviteLink", data=data)
