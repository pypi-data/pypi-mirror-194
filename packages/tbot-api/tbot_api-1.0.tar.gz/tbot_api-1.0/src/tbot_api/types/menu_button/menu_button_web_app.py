from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from ...enums import MenuButtonType
from .menu_button import MenuButton

if TYPE_CHECKING:
    from ..web_app_info import WebAppInfo


class MenuButtonWebApp(MenuButton):
    type: str = Field(MenuButtonType.WEB_APP, const=True)
    text: str
    web_app: WebAppInfo
