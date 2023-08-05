from enum import Enum


class InputMediaType(str, Enum):
    ANIMATION = "animation"
    AUDIO = "audio"
    DOCUMENT = "document"
    PHOTO = "photo"
    VIDEO = "video"
