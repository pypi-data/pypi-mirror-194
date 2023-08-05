from __future__ import annotations

from pydantic import Field

from ...enums import MenuButtonType
from .menu_button import MenuButton


class MenuButtonDefault(MenuButton):
    type: str = Field(MenuButtonType.DEFAULT, const=True)
