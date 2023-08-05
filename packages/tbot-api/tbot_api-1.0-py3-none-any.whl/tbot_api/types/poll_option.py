from __future__ import annotations

from .base import TelegramObject


class PollOption(TelegramObject):
    text: str
    voter_count: int
