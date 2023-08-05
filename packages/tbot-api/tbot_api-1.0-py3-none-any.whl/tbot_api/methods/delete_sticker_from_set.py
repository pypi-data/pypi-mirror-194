from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class DeleteStickerFromSet(TelegramMethod[bool]):
    __returns__ = bool

    sticker: str

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="deleteStickerFromSet", data=data)
