from __future__ import annotations

from typing import TYPE_CHECKING, List

from .base import MutableTelegramObject

if TYPE_CHECKING:
    from .inline_keyboard_button import InlineKeyboardButton


class InlineKeyboardMarkup(MutableTelegramObject):
    inline_keyboard: List[List[InlineKeyboardButton]]
