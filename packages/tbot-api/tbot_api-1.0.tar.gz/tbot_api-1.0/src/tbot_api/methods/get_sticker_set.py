from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..types import StickerSet
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetStickerSet(TelegramMethod[StickerSet]):
    __returns__ = StickerSet

    name: str

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getStickerSet", data=data)
