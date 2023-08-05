from __future__ import annotations

from .base import TelegramObject


class WebAppData(TelegramObject):
    data: str
    button_text: str
