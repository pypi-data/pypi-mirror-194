from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import DeleteStickerFromSet, SetStickerPositionInSet
    from .file import File
    from .mask_position import MaskPosition
    from .photo_size import PhotoSize


class Sticker(TelegramObject):
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumb: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    premium_animation: Optional[File] = None
    mask_position: Optional[MaskPosition] = None
    custom_emoji_id: Optional[str] = None
    file_size: Optional[int] = None

    def set_position_in_set(
        self,
        position: int,
        **kwargs: Dict,
    ) -> SetStickerPositionInSet:
        from ..methods import SetStickerPositionInSet

        return SetStickerPositionInSet(
            sticker=self.file_id,
            position=position,
            **kwargs,
        )

    def delete_from_set(
        self,
        **kwargs: Dict,
    ) -> DeleteStickerFromSet:
        from ..methods import DeleteStickerFromSet

        return DeleteStickerFromSet(
            sticker=self.file_id,
            **kwargs,
        )
