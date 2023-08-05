from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union

from ..types import Chat
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetChat(TelegramMethod[Chat]):
    __returns__ = Chat

    chat_id: Union[int, str]

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getChat", data=data)
