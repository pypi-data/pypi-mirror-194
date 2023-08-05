from __future__ import annotations

from pydantic import Field

from .passport_element_error import PassportElementError


class PassportElementErrorUnspecified(PassportElementError):
    source: str = Field("unspecified", const=True)
    type: str
    element_hash: str
    message: str
