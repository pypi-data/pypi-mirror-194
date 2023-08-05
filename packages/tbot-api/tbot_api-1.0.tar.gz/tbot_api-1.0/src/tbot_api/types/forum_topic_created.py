from __future__ import annotations

from typing import Optional

from .base import TelegramObject


class ForumTopicCreated(TelegramObject):
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None
