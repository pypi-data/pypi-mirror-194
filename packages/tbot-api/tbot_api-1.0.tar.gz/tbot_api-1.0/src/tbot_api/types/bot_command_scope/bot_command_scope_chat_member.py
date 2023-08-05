from __future__ import annotations

from typing import Union

from pydantic import Field

from ...enums import BotCommandScopeType
from .bot_command_scope import BotCommandScope


class BotCommandScopeChatMember(BotCommandScope):
    type: str = Field(BotCommandScopeType.CHAT_MEMBER, const=True)

    chat_id: Union[int, str]

    user_id: int
