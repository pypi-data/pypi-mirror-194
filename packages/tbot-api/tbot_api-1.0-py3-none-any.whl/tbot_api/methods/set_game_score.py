from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import Message
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class SetGameScore(TelegramMethod[Union[bool, Message]]):
    __returns__ = Union[bool, Message]

    user_id: int
    score: int
    force: Optional[bool] = None
    disable_edit_message: Optional[bool] = None
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="setGameScore", data=data)
