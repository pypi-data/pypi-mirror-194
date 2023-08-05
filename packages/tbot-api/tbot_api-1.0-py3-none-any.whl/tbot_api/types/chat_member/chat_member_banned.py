from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import Field

from ...enums import ChatMemberStatus
from .chat_member import ChatMember

if TYPE_CHECKING:
    from ..user import User


class ChatMemberBanned(ChatMember):
    status: str = Field(ChatMemberStatus.KICKED, const=True)
    user: User
    until_date: datetime
