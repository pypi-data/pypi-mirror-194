from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import ForumTopic
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class CreateForumTopic(TelegramMethod[ForumTopic]):
    __returns__ = ForumTopic

    chat_id: Union[int, str]
    name: str
    icon_color: Optional[int] = None
    icon_custom_emoji_id: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="createForumTopic", data=data)
