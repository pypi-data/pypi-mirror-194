from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..base import MutableTelegramObject

if TYPE_CHECKING:
    from ..web_app_info import WebAppInfo


class MenuButton(MutableTelegramObject):
    type: str
    text: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
