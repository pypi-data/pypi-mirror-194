from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..types import (
    ForceReply,
    InlineKeyboardMarkup,
    InputFile,
    Message,
    MessageEntity,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from .base import Request, TelegramMethod, prepare_file, prepare_parse_mode

if TYPE_CHECKING:
    from ..bot import Bot


class SendAnimation(TelegramMethod[Message]):
    __returns__ = Message

    chat_id: Union[int, str]
    animation: Union[InputFile, str]
    message_thread_id: Optional[int] = None
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    thumb: Optional[Union[InputFile, str]] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    has_spoiler: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_to_message_id: Optional[int] = None
    allow_sending_without_reply: Optional[bool] = None
    reply_markup: Optional[
        Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
    ] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict(exclude={"animation", "thumb"})

        prepare_parse_mode(
            bot, data, parse_mode_property="parse_mode", entities_property="caption_entities"
        )

        files: Dict[str, InputFile] = {}
        prepare_file(data=data, files=files, name="animation", value=self.animation)
        prepare_file(data=data, files=files, name="thumb", value=self.thumb)

        return Request(method="sendAnimation", data=data, files=files)
