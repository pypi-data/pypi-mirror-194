from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..types import User
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetMe(TelegramMethod[User]):
    __returns__ = User

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getMe", data=data)
