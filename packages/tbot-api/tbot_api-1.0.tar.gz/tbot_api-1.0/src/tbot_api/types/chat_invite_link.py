from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from .base import TelegramObject

if TYPE_CHECKING:
    from .user import User


class ChatInviteLink(TelegramObject):
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: Optional[str] = None
    expire_date: Optional[datetime] = None
    member_limit: Optional[int] = None
    pending_join_request_count: Optional[int] = None
