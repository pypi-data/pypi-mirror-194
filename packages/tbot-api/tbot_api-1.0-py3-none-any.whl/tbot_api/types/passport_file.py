from __future__ import annotations

from .base import TelegramObject


class PassportFile(TelegramObject):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int
