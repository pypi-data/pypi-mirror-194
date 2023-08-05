from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from ...enums import ChatMemberStatus
from .chat_member import ChatMember

if TYPE_CHECKING:
    from ..user import User


class ChatMemberAdministrator(ChatMember):
    status: str = Field(ChatMemberStatus.ADMINISTRATOR, const=True)
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    custom_title: Optional[str] = None
