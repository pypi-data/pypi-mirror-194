from __future__ import annotations

from pydantic import Field

from ...enums import BotCommandScopeType
from .bot_command_scope import BotCommandScope


class BotCommandScopeAllPrivateChats(BotCommandScope):
    type: str = Field(BotCommandScopeType.ALL_PRIVATE_CHATS, const=True)
