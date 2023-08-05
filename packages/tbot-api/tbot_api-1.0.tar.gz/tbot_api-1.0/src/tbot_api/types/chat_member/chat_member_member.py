from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from ...enums import ChatMemberStatus
from .chat_member import ChatMember

if TYPE_CHECKING:
    from ..user import User


class ChatMemberMember(ChatMember):
    status: str = Field(ChatMemberStatus.MEMBER, const=True)
    user: User
