from __future__ import annotations

from typing import Optional

from .base import TelegramObject


class Voice(TelegramObject):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
