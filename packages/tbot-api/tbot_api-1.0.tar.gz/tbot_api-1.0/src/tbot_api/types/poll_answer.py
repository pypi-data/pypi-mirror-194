from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from .user import User


class PollAnswer(TelegramObject):
    poll_id: str
    from_user: User = Field(..., alias="user")
    option_ids: List[int]
