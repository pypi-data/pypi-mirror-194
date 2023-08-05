from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..types import (
    ForceReply,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from .base import Request, TelegramMethod, prepare_parse_mode

if TYPE_CHECKING:
    from ..bot import Bot


class SendMessage(TelegramMethod[Message]):
    __returns__ = Message

    chat_id: Union[int, str]
    text: str
    message_thread_id: Optional[int] = None
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    disable_web_page_preview: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_to_message_id: Optional[int] = None
    allow_sending_without_reply: Optional[bool] = None
    reply_markup: Optional[
        Union[
            InlineKeyboardMarkup,
            ReplyKeyboardMarkup,
            ReplyKeyboardRemove,
            ForceReply,
        ]
    ] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        prepare_parse_mode(
            bot, data, parse_mode_property="parse_mode", entities_property="entities"
        )

        return Request(method="sendMessage", data=data)
