from __future__ import annotations

from .base import TelegramObject


class Dice(TelegramObject):
    emoji: str
    value: int
