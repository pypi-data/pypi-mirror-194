from __future__ import annotations

from typing import Optional

from .base import TelegramObject


class SentWebAppMessage(TelegramObject):
    inline_message_id: Optional[str] = None
