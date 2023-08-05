from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Union

from ..types import (
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberRestricted,
)
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetChatAdministrators(
    TelegramMethod[
        List[
            Union[
                ChatMemberOwner,
                ChatMemberAdministrator,
                ChatMemberMember,
                ChatMemberRestricted,
                ChatMemberLeft,
                ChatMemberBanned,
            ]
        ]
    ]
):
    __returns__ = List[
        Union[
            ChatMemberOwner,
            ChatMemberAdministrator,
            ChatMemberMember,
            ChatMemberRestricted,
            ChatMemberLeft,
            ChatMemberBanned,
        ]
    ]

    chat_id: Union[int, str]

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getChatAdministrators", data=data)
