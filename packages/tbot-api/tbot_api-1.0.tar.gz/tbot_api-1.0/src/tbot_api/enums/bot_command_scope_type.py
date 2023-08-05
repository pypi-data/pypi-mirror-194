from enum import Enum


class BotCommandScopeType(str, Enum):
    DEFAULT = "default"
    ALL_PRIVATE_CHATS = "all_private_chats"
    ALL_GROUP_CHATS = "all_group_chats"
    ALL_CHAT_ADMINISTRATORS = "all_chat_administrators"
    CHAT = "chat"
    CHAT_ADMINISTRATORS = "chat_administrators"
    CHAT_MEMBER = "chat_member"
