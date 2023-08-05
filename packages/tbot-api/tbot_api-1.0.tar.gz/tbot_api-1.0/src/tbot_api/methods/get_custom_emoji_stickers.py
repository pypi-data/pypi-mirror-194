from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from ..types import Sticker
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetCustomEmojiStickers(TelegramMethod[List[Sticker]]):
    __returns__ = List[Sticker]

    custom_emoji_ids: List[str]

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getCustomEmojiStickers", data=data)
