from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import (
    ForceReply,
    InlineKeyboardMarkup,
    InputFile,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from .base import Request, TelegramMethod, prepare_file

if TYPE_CHECKING:
    from ..bot import Bot


class SendVideoNote(TelegramMethod[Message]):
    __returns__ = Message

    chat_id: Union[int, str]
    video_note: Union[str, InputFile]
    message_thread_id: Optional[int] = None
    duration: Optional[int] = None
    length: Optional[int] = None
    thumb: Optional[Union[str, InputFile]] = None
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
        data: Dict[str, Any] = self.dict(exclude={"video_note", "thumb"})

        files: Dict[str, InputFile] = {}
        prepare_file(data=data, files=files, name="video_note", value=self.video_note)
        prepare_file(data=data, files=files, name="thumb", value=self.thumb)

        return Request(method="sendVideoNote", data=data, files=files)
