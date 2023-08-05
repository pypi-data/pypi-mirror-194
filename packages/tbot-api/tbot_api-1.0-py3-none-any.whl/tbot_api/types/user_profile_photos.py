from __future__ import annotations

from typing import TYPE_CHECKING, List

from .base import TelegramObject

if TYPE_CHECKING:
    from .photo_size import PhotoSize


class UserProfilePhotos(TelegramObject):
    total_count: int
    photos: List[List[PhotoSize]]
