from __future__ import annotations

from datetime import datetime

from .base import TelegramObject


class VideoChatScheduled(TelegramObject):
    start_date: datetime
