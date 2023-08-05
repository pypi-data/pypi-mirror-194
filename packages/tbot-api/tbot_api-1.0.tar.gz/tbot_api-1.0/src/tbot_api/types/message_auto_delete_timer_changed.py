from __future__ import annotations

from .base import TelegramObject


class MessageAutoDeleteTimerChanged(TelegramObject):
    message_auto_delete_time: int
