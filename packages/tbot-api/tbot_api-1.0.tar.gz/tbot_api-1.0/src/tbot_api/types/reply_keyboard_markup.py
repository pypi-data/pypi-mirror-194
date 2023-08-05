from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .base import MutableTelegramObject

if TYPE_CHECKING:
    from .keyboard_button import KeyboardButton


class ReplyKeyboardMarkup(MutableTelegramObject):
    keyboard: List[List[KeyboardButton]]
    is_persistent: Optional[bool] = None
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
