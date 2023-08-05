from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union

from ..types import ChatInviteLink
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class RevokeChatInviteLink(TelegramMethod[ChatInviteLink]):
    __returns__ = ChatInviteLink

    chat_id: Union[int, str]
    invite_link: str

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="revokeChatInviteLink", data=data)
