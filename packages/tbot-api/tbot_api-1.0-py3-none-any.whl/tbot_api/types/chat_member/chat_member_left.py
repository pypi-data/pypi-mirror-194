from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from ...enums import ChatMemberStatus
from .chat_member import ChatMember

if TYPE_CHECKING:
    from ..user import User


class ChatMemberLeft(ChatMember):
    status: str = Field(ChatMemberStatus.LEFT, const=True)
    user: User
