from enum import Enum


class MenuButtonType(str, Enum):
    DEFAULT = "default"
    COMMANDS = "commands"
    WEB_APP = "web_app"
