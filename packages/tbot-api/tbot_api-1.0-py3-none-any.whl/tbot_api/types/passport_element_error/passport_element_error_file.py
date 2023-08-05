from __future__ import annotations

from pydantic import Field

from .passport_element_error import PassportElementError


class PassportElementErrorFile(PassportElementError):
    source: str = Field("file", const=True)
    type: str
    file_hash: str
    message: str
