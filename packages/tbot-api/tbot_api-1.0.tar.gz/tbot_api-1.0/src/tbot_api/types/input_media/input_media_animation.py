from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from pydantic import Field

from ...enums import InputMediaType
from .input_media import InputMedia

if TYPE_CHECKING:
    from ..input_file import InputFile
    from ..message_entity import MessageEntity


class InputMediaAnimation(InputMedia):
    type: str = Field(InputMediaType.ANIMATION, const=True)
    media: Union[str, InputFile]
    thumb: Optional[Union[InputFile, str]] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    has_spoiler: Optional[bool] = None
