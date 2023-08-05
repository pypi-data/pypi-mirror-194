from __future__ import annotations

from pydantic import Field

from ...enums import MenuButtonType
from .menu_button import MenuButton


class MenuButtonCommands(MenuButton):
    type: str = Field(MenuButtonType.COMMANDS, const=True)
