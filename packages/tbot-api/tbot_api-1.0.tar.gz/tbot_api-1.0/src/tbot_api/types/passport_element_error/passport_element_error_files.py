from __future__ import annotations

from typing import List

from pydantic import Field

from .passport_element_error import PassportElementError


class PassportElementErrorFiles(PassportElementError):
    source: str = Field("files", const=True)
    type: str
    file_hashes: List[str]
    message: str
