from __future__ import annotations

from typing import Optional

from .base import MutableTelegramObject


class KeyboardButtonPollType(MutableTelegramObject):
    type: Optional[str] = None
