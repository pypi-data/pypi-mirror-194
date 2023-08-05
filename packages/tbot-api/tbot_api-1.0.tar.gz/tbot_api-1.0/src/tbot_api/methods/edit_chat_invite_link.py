from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import ChatInviteLink
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class EditChatInviteLink(TelegramMethod[ChatInviteLink]):
    __returns__ = ChatInviteLink

    chat_id: Union[int, str]
    invite_link: str
    name: Optional[str] = None
    expire_date: Optional[Union[int, datetime, timedelta]] = None
    member_limit: Optional[int] = None
    creates_join_request: Optional[bool] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="editChatInviteLink", data=data)
