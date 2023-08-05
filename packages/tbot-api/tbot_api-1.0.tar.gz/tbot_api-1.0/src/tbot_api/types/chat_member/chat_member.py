from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from ..base import TelegramObject

if TYPE_CHECKING:
    from ..user import User


class ChatMember(TelegramObject):
    status: str
    user: Optional[User] = None
    is_anonymous: Optional[bool] = None
    custom_title: Optional[str] = None
    can_be_edited: Optional[bool] = None
    can_manage_chat: Optional[bool] = None
    can_delete_messages: Optional[bool] = None
    can_manage_video_chats: Optional[bool] = None
    can_restrict_members: Optional[bool] = None
    can_promote_members: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    is_member: Optional[bool] = None
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    until_date: Optional[datetime] = None
