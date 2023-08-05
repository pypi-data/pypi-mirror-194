from __future__ import annotations

from typing import Optional

from .input_message_content import InputMessageContent


class InputContactMessageContent(InputMessageContent):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    vcard: Optional[str] = None
