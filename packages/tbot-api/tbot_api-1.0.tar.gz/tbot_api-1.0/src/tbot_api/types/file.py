from __future__ import annotations

from typing import Optional

from .base import TelegramObject


class File(TelegramObject):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None
