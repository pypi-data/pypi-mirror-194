from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from .location import Location
    from .user import User


class ChosenInlineResult(TelegramObject):
    result_id: str
    from_user: User = Field(..., alias="from")
    query: str
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None
