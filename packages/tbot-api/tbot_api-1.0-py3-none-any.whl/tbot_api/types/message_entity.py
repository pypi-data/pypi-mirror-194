from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .base import MutableTelegramObject

if TYPE_CHECKING:
    from .user import User


class MessageEntity(MutableTelegramObject):
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None

    def extract_from(self, text: str) -> str:
        return text.encode("utf=16=le")[self.offset * 2 : (self.offset + self.length) * 2].decode(
            "utf-16-le"
        )
