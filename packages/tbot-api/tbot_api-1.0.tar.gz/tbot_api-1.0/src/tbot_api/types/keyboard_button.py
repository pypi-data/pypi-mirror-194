from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .base import MutableTelegramObject

if TYPE_CHECKING:
    from .keyboard_button_poll_type import KeyboardButtonPollType
    from .web_app_info import WebAppInfo


class KeyboardButton(MutableTelegramObject):
    text: str
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None
