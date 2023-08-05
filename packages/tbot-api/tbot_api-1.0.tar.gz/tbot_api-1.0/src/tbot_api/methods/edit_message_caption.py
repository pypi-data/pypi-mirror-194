from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..types import InlineKeyboardMarkup, Message, MessageEntity
from .base import Request, TelegramMethod, prepare_parse_mode

if TYPE_CHECKING:
    from ..bot import Bot


class EditMessageCaption(TelegramMethod[Union[bool, Message]]):
    __returns__ = Union[bool, Message]

    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        prepare_parse_mode(
            bot, data, parse_mode_property="parse_mode", entities_property="caption_entities"
        )

        return Request(method="editMessageCaption", data=data)
