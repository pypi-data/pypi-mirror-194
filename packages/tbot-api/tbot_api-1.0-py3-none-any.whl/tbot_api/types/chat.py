from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import (
        BanChatMember,
        BanChatSenderChat,
        CreateChatInviteLink,
        DeleteChatPhoto,
        DeleteChatStickerSet,
        DeleteMessage,
        EditChatInviteLink,
        ExportChatInviteLink,
        GetChatAdministrators,
        GetChatMember,
        GetChatMemberCount,
        LeaveChat,
        PinChatMessage,
        PromoteChatMember,
        RestrictChatMember,
        RevokeChatInviteLink,
        SendChatAction,
        SetChatAdministratorCustomTitle,
        SetChatDescription,
        SetChatPermissions,
        SetChatPhoto,
        SetChatStickerSet,
        SetChatTitle,
        UnbanChatMember,
        UnbanChatSenderChat,
        UnpinAllChatMessages,
        UnpinChatMessage,
    )
    from .chat_location import ChatLocation
    from .chat_permissions import ChatPermissions
    from .chat_photo import ChatPhoto
    from .input_file import InputFile
    from .message import Message


class Chat(TelegramObject):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None
    photo: Optional[ChatPhoto] = None
    active_usernames: Optional[List[str]] = None
    emoji_status_custom_emoji_id: Optional[str] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[bool] = None
    has_restricted_voice_and_video_messages: Optional[bool] = None
    join_to_send_messages: Optional[bool] = None
    join_by_request: Optional[bool] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional[Message] = None
    permissions: Optional[ChatPermissions] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_protected_content: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None

    def ban_sender_chat(
        self,
        sender_chat_id: int,
        **kwargs: Dict,
    ) -> BanChatSenderChat:
        from ..methods import BanChatSenderChat

        return BanChatSenderChat(
            chat_id=self.id,
            sender_chat_id=sender_chat_id,
            **kwargs,
        )

    def unban_sender_chat(
        self,
        sender_chat_id: int,
        **kwargs: Dict,
    ) -> UnbanChatSenderChat:
        from ..methods import UnbanChatSenderChat

        return UnbanChatSenderChat(
            chat_id=self.id,
            sender_chat_id=sender_chat_id,
            **kwargs,
        )

    def get_administrators(
        self,
        **kwargs: Dict,
    ) -> GetChatAdministrators:
        from ..methods import GetChatAdministrators

        return GetChatAdministrators(
            chat_id=self.id,
            **kwargs,
        )

    def delete_message(
        self,
        message_id: int,
        **kwargs: Dict,
    ) -> DeleteMessage:
        from ..methods import DeleteMessage

        return DeleteMessage(
            chat_id=self.id,
            message_id=message_id,
            **kwargs,
        )

    def revoke_invite_link(
        self,
        invite_link: str,
        **kwargs: Dict,
    ) -> RevokeChatInviteLink:
        from ..methods import RevokeChatInviteLink

        return RevokeChatInviteLink(
            chat_id=self.id,
            invite_link=invite_link,
            **kwargs,
        )

    def edit_invite_link(
        self,
        invite_link: str,
        name: Optional[str] = None,
        expire_date: Optional[Union[int, datetime, timedelta]] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
        **kwargs: Dict,
    ) -> EditChatInviteLink:
        from ..methods import EditChatInviteLink

        return EditChatInviteLink(
            chat_id=self.id,
            invite_link=invite_link,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
            **kwargs,
        )

    def create_invite_link(
        self,
        name: Optional[str] = None,
        expire_date: Optional[Union[int, datetime, timedelta]] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
        **kwargs: Dict,
    ) -> CreateChatInviteLink:
        from ..methods import CreateChatInviteLink

        return CreateChatInviteLink(
            chat_id=self.id,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
            **kwargs,
        )

    def export_invite_link(
        self,
        **kwargs: Dict,
    ) -> ExportChatInviteLink:
        from ..methods import ExportChatInviteLink

        return ExportChatInviteLink(
            chat_id=self.id,
            **kwargs,
        )

    def do(
        self,
        action: str,
        **kwargs: Dict,
    ) -> SendChatAction:
        from ..methods import SendChatAction

        return SendChatAction(
            chat_id=self.id,
            action=action,
            **kwargs,
        )

    def delete_sticker_set(
        self,
        **kwargs: Dict,
    ) -> DeleteChatStickerSet:
        from ..methods import DeleteChatStickerSet

        return DeleteChatStickerSet(
            chat_id=self.id,
            **kwargs,
        )

    def set_sticker_set(
        self,
        sticker_set_name: str,
        **kwargs: Dict,
    ) -> SetChatStickerSet:
        from ..methods import SetChatStickerSet

        return SetChatStickerSet(
            chat_id=self.id,
            sticker_set_name=sticker_set_name,
            **kwargs,
        )

    def get_member(
        self,
        user_id: int,
        **kwargs: Dict,
    ) -> GetChatMember:
        from ..methods import GetChatMember

        return GetChatMember(
            chat_id=self.id,
            user_id=user_id,
            **kwargs,
        )

    def get_member_count(
        self,
        **kwargs: Dict,
    ) -> GetChatMemberCount:
        from ..methods import GetChatMemberCount

        return GetChatMemberCount(
            chat_id=self.id,
            **kwargs,
        )

    def leave(
        self,
        **kwargs: Dict,
    ) -> LeaveChat:
        from ..methods import LeaveChat

        return LeaveChat(
            chat_id=self.id,
            **kwargs,
        )

    def unpin_all_messages(
        self,
        **kwargs: Dict,
    ) -> UnpinAllChatMessages:
        from ..methods import UnpinAllChatMessages

        return UnpinAllChatMessages(
            chat_id=self.id,
            **kwargs,
        )

    def unpin_message(
        self,
        message_id: Optional[int] = None,
        **kwargs: Dict,
    ) -> UnpinChatMessage:
        from ..methods import UnpinChatMessage

        return UnpinChatMessage(
            chat_id=self.id,
            message_id=message_id,
            **kwargs,
        )

    def pin_message(
        self,
        message_id: int,
        disable_notification: Optional[bool] = None,
        **kwargs: Dict,
    ) -> PinChatMessage:
        from ..methods import PinChatMessage

        return PinChatMessage(
            chat_id=self.id,
            message_id=message_id,
            disable_notification=disable_notification,
            **kwargs,
        )

    def set_administrator_custom_title(
        self,
        user_id: int,
        custom_title: str,
        **kwargs: Dict,
    ) -> SetChatAdministratorCustomTitle:
        from ..methods import SetChatAdministratorCustomTitle

        return SetChatAdministratorCustomTitle(
            chat_id=self.id,
            user_id=user_id,
            custom_title=custom_title,
            **kwargs,
        )

    def set_permissions(
        self,
        permissions: ChatPermissions,
        **kwargs: Dict,
    ) -> SetChatPermissions:
        from ..methods import SetChatPermissions

        return SetChatPermissions(
            chat_id=self.id,
            permissions=permissions,
            **kwargs,
        )

    def promote(
        self,
        user_id: int,
        is_anonymous: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_manage_video_chats: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None,
        **kwargs: Dict,
    ) -> PromoteChatMember:
        from ..methods import PromoteChatMember

        return PromoteChatMember(
            chat_id=self.id,
            user_id=user_id,
            is_anonymous=is_anonymous,
            can_manage_chat=can_manage_chat,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_delete_messages=can_delete_messages,
            can_manage_video_chats=can_manage_video_chats,
            can_restrict_members=can_restrict_members,
            can_promote_members=can_promote_members,
            can_change_info=can_change_info,
            can_invite_users=can_invite_users,
            can_pin_messages=can_pin_messages,
            can_manage_topics=can_manage_topics,
            **kwargs,
        )

    def restrict(
        self,
        user_id: int,
        permissions: ChatPermissions,
        until_date: Optional[Union[int, datetime, timedelta]] = None,
        **kwargs: Dict,
    ) -> RestrictChatMember:
        from ..methods import RestrictChatMember

        return RestrictChatMember(
            chat_id=self.id,
            user_id=user_id,
            permissions=permissions,
            until_date=until_date,
            **kwargs,
        )

    def unban(
        self,
        user_id: int,
        only_if_banned: Optional[bool] = None,
        **kwargs: Dict,
    ) -> UnbanChatMember:
        from ..methods import UnbanChatMember

        return UnbanChatMember(
            chat_id=self.id,
            user_id=user_id,
            only_if_banned=only_if_banned,
            **kwargs,
        )

    def ban(
        self,
        user_id: int,
        until_date: Optional[Union[int, datetime, timedelta]] = None,
        revoke_messages: Optional[bool] = None,
        **kwargs: Dict,
    ) -> BanChatMember:
        from ..methods import BanChatMember

        return BanChatMember(
            chat_id=self.id,
            user_id=user_id,
            until_date=until_date,
            revoke_messages=revoke_messages,
            **kwargs,
        )

    def set_description(
        self,
        description: Optional[str] = None,
        **kwargs: Dict,
    ) -> SetChatDescription:
        from ..methods import SetChatDescription

        return SetChatDescription(
            chat_id=self.id,
            description=description,
            **kwargs,
        )

    def set_title(
        self,
        title: str,
        **kwargs: Dict,
    ) -> SetChatTitle:
        from ..methods import SetChatTitle

        return SetChatTitle(
            chat_id=self.id,
            title=title,
            **kwargs,
        )

    def delete_photo(
        self,
        **kwargs: Dict,
    ) -> DeleteChatPhoto:
        from ..methods import DeleteChatPhoto

        return DeleteChatPhoto(
            chat_id=self.id,
            **kwargs,
        )

    def set_photo(
        self,
        photo: InputFile,
        **kwargs: Dict,
    ) -> SetChatPhoto:
        from ..methods import SetChatPhoto

        return SetChatPhoto(
            chat_id=self.id,
            photo=photo,
            **kwargs,
        )
