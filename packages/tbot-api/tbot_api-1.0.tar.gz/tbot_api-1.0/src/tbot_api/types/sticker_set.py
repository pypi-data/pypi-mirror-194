from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .base import TelegramObject

if TYPE_CHECKING:
    from .photo_size import PhotoSize
    from .sticker import Sticker


class StickerSet(TelegramObject):
    name: str
    title: str
    sticker_type: str
    is_animated: bool
    is_video: bool
    stickers: List[Sticker]
    thumb: Optional[PhotoSize] = None
