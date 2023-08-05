from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import UserProfilePhotos
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetUserProfilePhotos(TelegramMethod[UserProfilePhotos]):
    __returns__ = UserProfilePhotos

    user_id: int
    offset: Optional[int] = None
    limit: Optional[int] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getUserProfilePhotos", data=data)
