from __future__ import annotations

from .base import TelegramObject


class MessageId(TelegramObject):
    message_id: int
