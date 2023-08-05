from __future__ import annotations

from pydantic import Field

from .passport_element_error import PassportElementError


class PassportElementErrorDataField(PassportElementError):
    source: str = Field("data", const=True)
    type: str
    field_name: str
    data_hash: str
    message: str
