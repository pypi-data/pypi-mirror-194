from __future__ import annotations

from typing import Optional

from .base import TelegramObject


class LoginUrl(TelegramObject):
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None
