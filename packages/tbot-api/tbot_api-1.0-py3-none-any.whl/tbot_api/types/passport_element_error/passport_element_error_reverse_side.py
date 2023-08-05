from __future__ import annotations

from pydantic import Field

from .passport_element_error import PassportElementError


class PassportElementErrorReverseSide(PassportElementError):
    source: str = Field("reverse_side", const=True)
    type: str
    file_hash: str
    message: str
