from __future__ import annotations

from .base import TelegramObject


class ChatPhoto(TelegramObject):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str
