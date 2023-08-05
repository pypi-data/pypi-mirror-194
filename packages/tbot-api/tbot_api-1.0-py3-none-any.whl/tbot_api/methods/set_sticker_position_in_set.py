from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class SetStickerPositionInSet(TelegramMethod[bool]):
    __returns__ = bool

    sticker: str
    position: int

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="setStickerPositionInSet", data=data)
