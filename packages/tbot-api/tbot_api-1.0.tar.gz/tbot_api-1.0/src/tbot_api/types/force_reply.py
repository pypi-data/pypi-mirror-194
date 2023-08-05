from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import MutableTelegramObject


class ForceReply(MutableTelegramObject):
    force_reply: bool = Field(True, const=True)
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
