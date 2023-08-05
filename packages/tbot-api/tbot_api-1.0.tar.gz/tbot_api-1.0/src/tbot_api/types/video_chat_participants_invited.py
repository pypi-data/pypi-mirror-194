from __future__ import annotations

from typing import TYPE_CHECKING, List

from .base import TelegramObject

if TYPE_CHECKING:
    from .user import User


class VideoChatParticipantsInvited(TelegramObject):
    users: List[User]
