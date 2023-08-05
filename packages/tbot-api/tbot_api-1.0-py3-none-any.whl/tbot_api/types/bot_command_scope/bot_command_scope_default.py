from __future__ import annotations

from pydantic import Field

from ...enums import BotCommandScopeType
from .bot_command_scope import BotCommandScope


class BotCommandScopeDefault(BotCommandScope):
    type: str = Field(BotCommandScopeType.DEFAULT, const=True)
