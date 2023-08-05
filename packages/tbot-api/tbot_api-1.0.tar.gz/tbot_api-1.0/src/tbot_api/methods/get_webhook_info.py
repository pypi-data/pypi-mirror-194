from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..types import WebhookInfo
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetWebhookInfo(TelegramMethod[WebhookInfo]):
    __returns__ = WebhookInfo

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getWebhookInfo", data=data)
