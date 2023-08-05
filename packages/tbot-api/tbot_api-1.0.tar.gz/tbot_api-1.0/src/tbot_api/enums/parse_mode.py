from enum import Enum


class ParseMode(str, Enum):
    MARKDOWN_V2 = "MarkdownV2"
    MARKDOWN = "Markdown"
    HTML = "HTML"
