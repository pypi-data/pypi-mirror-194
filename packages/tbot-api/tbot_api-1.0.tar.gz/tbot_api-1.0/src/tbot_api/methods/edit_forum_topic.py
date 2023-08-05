from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union

from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class EditForumTopic(TelegramMethod[bool]):
    __returns__ = bool

    chat_id: Union[int, str]
    message_thread_id: int
    name: str
    icon_custom_emoji_id: str

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="editForumTopic", data=data)
