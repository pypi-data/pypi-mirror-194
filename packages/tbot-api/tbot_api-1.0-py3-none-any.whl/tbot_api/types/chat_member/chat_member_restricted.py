from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import Field

from ...enums import ChatMemberStatus
from .chat_member import ChatMember

if TYPE_CHECKING:
    from ..user import User


class ChatMemberRestricted(ChatMember):
    status: str = Field(ChatMemberStatus.RESTRICTED, const=True)
    user: User
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: datetime
