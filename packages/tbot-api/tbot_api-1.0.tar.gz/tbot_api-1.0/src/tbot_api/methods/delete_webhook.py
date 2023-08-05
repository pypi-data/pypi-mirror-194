from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class DeleteWebhook(TelegramMethod[bool]):
    __returns__ = bool

    drop_pending_updates: Optional[bool] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="deleteWebhook", data=data)
