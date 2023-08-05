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


class SendDocument(TelegramMethod[Message]):
    __returns__ = Message

    chat_id: Union[int, str]
    document: Union[str, InputFile]
    message_thread_id: Optional[int] = None
    thumb: Optional[Union[str, InputFile]] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    disable_content_type_detection: Optional[bool] = None
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
        data: Dict[str, Any] = self.dict(exclude={"document", "thumb"})

        prepare_parse_mode(
            bot, data, parse_mode_property="parse_mode", entities_property="caption_entities"
        )

        files: Dict[str, InputFile] = {}
        prepare_file(data=data, files=files, name="document", value=self.document)
        prepare_file(data=data, files=files, name="thumb", value=self.thumb)

        return Request(method="sendDocument", data=data, files=files)
