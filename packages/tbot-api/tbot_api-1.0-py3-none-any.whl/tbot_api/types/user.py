from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import GetUserProfilePhotos


class User(TelegramObject):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None

    def get_profile_photos(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Dict,
    ) -> GetUserProfilePhotos:
        from ..methods import GetUserProfilePhotos

        return GetUserProfilePhotos(
            user_id=self.id,
            offset=offset,
            limit=limit,
            **kwargs,
        )
