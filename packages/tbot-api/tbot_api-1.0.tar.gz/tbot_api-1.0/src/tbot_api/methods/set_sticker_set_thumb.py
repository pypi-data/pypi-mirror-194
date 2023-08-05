from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import InputFile
from .base import Request, TelegramMethod, prepare_file

if TYPE_CHECKING:
    from ..bot import Bot


class SetStickerSetThumb(TelegramMethod[bool]):
    __returns__ = bool

    name: str
    user_id: int
    thumb: Optional[Union[str, InputFile]] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict(exclude={"thumb"})
        files: Dict[str, InputFile] = {}

        prepare_file(data=data, files=files, name="thumb", value=self.thumb)

        return Request(method="setStickerSetThumb", data=data, files=files)
