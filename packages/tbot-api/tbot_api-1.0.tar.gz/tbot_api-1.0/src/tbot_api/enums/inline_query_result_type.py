from enum import Enum


class InlineQueryResultType(str, Enum):
    AUDIO = "audio"
    DOCUMENT = "document"
    GIF = "gif"
    MPEG = "mpeg"
    PHOTO = "photo"
    STICKER = "sticker"
    VIDEO = "video"
    VOICE = "voice"
    ARTICLE = "article"
    CONTACT = "contact"
    GAME = "game"
    LOCATION = "location"
    VENUE = "venue"
