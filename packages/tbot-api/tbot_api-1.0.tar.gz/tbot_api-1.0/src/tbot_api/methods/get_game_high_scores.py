from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import GameHighScore
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetGameHighScores(TelegramMethod[List[GameHighScore]]):
    __returns__ = List[GameHighScore]

    user_id: int
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getGameHighScores", data=data)
