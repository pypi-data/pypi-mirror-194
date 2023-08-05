from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Update
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetUpdates(TelegramMethod[List[Update]]):
    __returns__ = List[Update]

    offset: Optional[int] = None
    limit: Optional[int] = None
    timeout: Optional[int] = None
    allowed_updates: Optional[List[str]] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getUpdates", data=data)
