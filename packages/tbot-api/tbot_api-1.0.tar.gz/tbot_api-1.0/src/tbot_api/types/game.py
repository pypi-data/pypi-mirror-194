from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .base import TelegramObject

if TYPE_CHECKING:
    from .animation import Animation
    from .message_entity import MessageEntity
    from .photo_size import PhotoSize


class Game(TelegramObject):
    title: str
    description: str
    photo: List[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None
