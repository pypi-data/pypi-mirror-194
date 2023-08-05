from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from .chat import Chat
    from .chat_invite_link import ChatInviteLink
    from .chat_member import (
        ChatMemberAdministrator,
        ChatMemberBanned,
        ChatMemberLeft,
        ChatMemberMember,
        ChatMemberOwner,
        ChatMemberRestricted,
    )
    from .user import User


class ChatMemberUpdated(TelegramObject):
    chat: Chat
    from_user: User = Field(..., alias="from")
    date: datetime
    old_chat_member: Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ]
    new_chat_member: Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ]
    invite_link: Optional[ChatInviteLink] = None
