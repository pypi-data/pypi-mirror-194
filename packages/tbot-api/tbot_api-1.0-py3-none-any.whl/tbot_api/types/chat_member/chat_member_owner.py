from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from ...enums import ChatMemberStatus
from .chat_member import ChatMember

if TYPE_CHECKING:
    from ..user import User


class ChatMemberOwner(ChatMember):
    status: str = Field(ChatMemberStatus.CREATOR, const=True)
    user: User
    is_anonymous: bool
    custom_title: Optional[str] = None
