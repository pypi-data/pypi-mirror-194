from __future__ import annotations

from pydantic import Field

from .passport_element_error import PassportElementError


class PassportElementErrorFrontSide(PassportElementError):
    source: str = Field("front_side", const=True)
    type: str
    file_hash: str
    message: str
