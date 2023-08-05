from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Dict, Optional

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import ApproveChatJoinRequest, DeclineChatJoinRequest
    from .chat import Chat
    from .chat_invite_link import ChatInviteLink
    from .user import User


class ChatJoinRequest(TelegramObject):
    chat: Chat
    from_user: User = Field(..., alias="from")
    date: datetime
    bio: Optional[str] = None
    invite_link: Optional[ChatInviteLink] = None

    def approve(
        self,
        **kwargs: Dict,
    ) -> ApproveChatJoinRequest:
        from ..methods import ApproveChatJoinRequest

        return ApproveChatJoinRequest(
            chat_id=self.chat.id,
            user_id=self.from_user.id,
            **kwargs,
        )

    def decline(
        self,
        **kwargs: Dict,
    ) -> DeclineChatJoinRequest:
        from ..methods import DeclineChatJoinRequest

        return DeclineChatJoinRequest(
            chat_id=self.chat.id,
            user_id=self.from_user.id,
            **kwargs,
        )
