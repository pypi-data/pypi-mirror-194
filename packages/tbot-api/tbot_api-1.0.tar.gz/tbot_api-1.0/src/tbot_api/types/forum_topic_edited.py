from typing import Optional

from .base import TelegramObject


class ForumTopicEdited(TelegramObject):
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None
