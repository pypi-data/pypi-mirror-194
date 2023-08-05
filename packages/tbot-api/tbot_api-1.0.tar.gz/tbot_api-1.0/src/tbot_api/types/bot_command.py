from __future__ import annotations

from .base import MutableTelegramObject


class BotCommand(MutableTelegramObject):
    command: str
    description: str
