from __future__ import annotations

from typing import List

from pydantic import Field

from .passport_element_error import PassportElementError


class PassportElementErrorTranslationFiles(PassportElementError):
    source: str = Field("translation_files", const=True)
    type: str
    file_hashes: List[str]
    message: str
