from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import InputFile, MaskPosition
from .base import Request, TelegramMethod, prepare_file

if TYPE_CHECKING:
    from ..bot import Bot


class AddStickerToSet(TelegramMethod[bool]):
    __returns__ = bool

    user_id: int
    name: str
    emojis: str
    png_sticker: Optional[Union[str, InputFile]] = None
    tgs_sticker: Optional[InputFile] = None
    webm_sticker: Optional[InputFile] = None
    mask_position: Optional[MaskPosition] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict(exclude={"png_sticker", "tgs_sticker", "webm_sticker"})

        files: Dict[str, InputFile] = {}
        prepare_file(data=data, files=files, name="png_sticker", value=self.png_sticker)
        prepare_file(data=data, files=files, name="tgs_sticker", value=self.tgs_sticker)
        prepare_file(data=data, files=files, name="webm_sticker", value=self.webm_sticker)

        return Request(method="addStickerToSet", data=data, files=files)
