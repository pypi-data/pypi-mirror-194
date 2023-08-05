from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import MutableTelegramObject


class ReplyKeyboardRemove(MutableTelegramObject):
    remove_keyboard: bool = Field(True, const=True)
    selective: Optional[bool] = None
