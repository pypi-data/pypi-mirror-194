import datetime
from typing import List, Optional, Union

from ..methods import (
    AddStickerToSet,
    AnswerCallbackQuery,
    AnswerInlineQuery,
    AnswerPreCheckoutQuery,
    AnswerShippingQuery,
    AnswerWebAppQuery,
    ApproveChatJoinRequest,
    BanChatMember,
    BanChatSenderChat,
    Close,
    CloseForumTopic,
    CloseGeneralForumTopic,
    CopyMessage,
    CreateChatInviteLink,
    CreateForumTopic,
    CreateInvoiceLink,
    CreateNewStickerSet,
    DeclineChatJoinRequest,
    DeleteChatPhoto,
    DeleteChatStickerSet,
    DeleteForumTopic,
    DeleteMessage,
    DeleteMyCommands,
    DeleteStickerFromSet,
    DeleteWebhook,
    EditChatInviteLink,
    EditForumTopic,
    EditGeneralForumTopic,
    EditMessageCaption,
    EditMessageLiveLocation,
    EditMessageMedia,
    EditMessageReplyMarkup,
    EditMessageText,
    ExportChatInviteLink,
    ForwardMessage,
    GetChat,
    GetChatAdministrators,
    GetChatMember,
    GetChatMemberCount,
    GetChatMenuButton,
    GetCustomEmojiStickers,
    GetFile,
    GetForumTopicIconStickers,
    GetGameHighScores,
    GetMe,
    GetMyCommands,
    GetMyDefaultAdministratorRights,
    GetStickerSet,
    GetUpdates,
    GetUserProfilePhotos,
    GetWebhookInfo,
    HideGeneralForumTopic,
    LeaveChat,
    LogOut,
    PinChatMessage,
    PromoteChatMember,
    ReopenForumTopic,
    ReopenGeneralForumTopic,
    RestrictChatMember,
    RevokeChatInviteLink,
    SendAnimation,
    SendAudio,
    SendChatAction,
    SendContact,
    SendDice,
    SendDocument,
    SendGame,
    SendInvoice,
    SendLocation,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
    SendPoll,
    SendSticker,
    SendVenue,
    SendVideo,
    SendVideoNote,
    SendVoice,
    SetChatAdministratorCustomTitle,
    SetChatDescription,
    SetChatMenuButton,
    SetChatPermissions,
    SetChatPhoto,
    SetChatStickerSet,
    SetChatTitle,
    SetGameScore,
    SetMyCommands,
    SetMyDefaultAdministratorRights,
    SetPassportDataErrors,
    SetStickerPositionInSet,
    SetStickerSetThumb,
    SetWebhook,
    StopMessageLiveLocation,
    StopPoll,
    TelegramMethod,
    TelegramType,
    UnbanChatMember,
    UnbanChatSenderChat,
    UnhideGeneralForumTopic,
    UnpinAllChatMessages,
    UnpinAllForumTopicMessages,
    UnpinChatMessage,
    UploadStickerFile,
)
from ..telegram import TELEGRAM_SERVER_PRODUCTION, TelegramAPIServer
from ..types import (
    BotCommand,
    BotCommandScope,
    Chat,
    ChatAdministratorRights,
    ChatInviteLink,
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberRestricted,
    ChatPermissions,
    File,
    ForceReply,
    ForumTopic,
    GameHighScore,
    InlineKeyboardMarkup,
    InlineQueryResult,
    InputFile,
    InputMedia,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    LabeledPrice,
    MaskPosition,
    MenuButtonCommands,
    MenuButtonDefault,
    MenuButtonWebApp,
    Message,
    MessageEntity,
    MessageId,
    PassportElementError,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    SentWebAppMessage,
    ShippingOption,
    Sticker,
    StickerSet,
    Update,
    User,
    UserProfilePhotos,
    WebhookInfo,
)


class Methods:
    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        emojis: str,
        png_sticker: Optional[Union[InputFile, str]] = None,
        tgs_sticker: Optional[InputFile] = None,
        webm_sticker: Optional[InputFile] = None,
        mask_position: Optional[MaskPosition] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = AddStickerToSet(
            user_id=user_id,
            name=name,
            emojis=emojis,
            png_sticker=png_sticker,
            tgs_sticker=tgs_sticker,
            webm_sticker=webm_sticker,
            mask_position=mask_position,
        )
        return await self.request(call, timeout=request_timeout)

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = AnswerCallbackQuery(
            callback_query_id=callback_query_id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )
        return await self.request(call, timeout=request_timeout)

    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: List[InlineQueryResult],
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        switch_pm_text: Optional[str] = None,
        switch_pm_parameter: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = AnswerInlineQuery(
            inline_query_id=inline_query_id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
        )
        return await self.request(call, timeout=request_timeout)

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        error_message: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = AnswerPreCheckoutQuery(
            pre_checkout_query_id=pre_checkout_query_id,
            ok=ok,
            error_message=error_message,
        )
        return await self.request(call, timeout=request_timeout)

    async def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        shipping_options: Optional[List[ShippingOption]] = None,
        error_message: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = AnswerShippingQuery(
            shipping_query_id=shipping_query_id,
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message,
        )
        return await self.request(call, timeout=request_timeout)

    async def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: InlineQueryResult,
        request_timeout: Optional[int] = None,
    ) -> SentWebAppMessage:
        call = AnswerWebAppQuery(
            web_app_query_id=web_app_query_id,
            result=result,
        )
        return await self.request(call, timeout=request_timeout)

    async def approve_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = ApproveChatJoinRequest(
            chat_id=chat_id,
            user_id=user_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        until_date: Optional[Union[datetime.datetime, datetime.timedelta, int]] = None,
        revoke_messages: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = BanChatMember(
            chat_id=chat_id,
            user_id=user_id,
            until_date=until_date,
            revoke_messages=revoke_messages,
        )
        return await self.request(call, timeout=request_timeout)

    async def ban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = BanChatSenderChat(
            chat_id=chat_id,
            sender_chat_id=sender_chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def close(
        self,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = Close()
        return await self.request(call, timeout=request_timeout)

    async def close_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = CloseForumTopic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def copy_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> MessageId:
        call = CopyMessage(
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
            message_thread_id=message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def create_chat_invite_link(
        self,
        chat_id: Union[int, str],
        name: Optional[str] = None,
        expire_date: Optional[Union[datetime.datetime, datetime.timedelta, int]] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> ChatInviteLink:
        call = CreateChatInviteLink(
            chat_id=chat_id,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        )
        return await self.request(call, timeout=request_timeout)

    async def create_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
        icon_color: Optional[int] = None,
        icon_custom_emoji_id: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> ForumTopic:
        call = CreateForumTopic(
            chat_id=chat_id,
            name=name,
            icon_color=icon_color,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: List[LabeledPrice],
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> str:
        call = CreateInvoiceLink(
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
        )
        return await self.request(call, timeout=request_timeout)

    async def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        emojis: str,
        png_sticker: Optional[Union[InputFile, str]] = None,
        tgs_sticker: Optional[InputFile] = None,
        webm_sticker: Optional[InputFile] = None,
        sticker_type: Optional[str] = None,
        mask_position: Optional[MaskPosition] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = CreateNewStickerSet(
            user_id=user_id,
            name=name,
            title=title,
            emojis=emojis,
            png_sticker=png_sticker,
            tgs_sticker=tgs_sticker,
            webm_sticker=webm_sticker,
            sticker_type=sticker_type,
            mask_position=mask_position,
        )
        return await self.request(call, timeout=request_timeout)

    async def decline_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = DeclineChatJoinRequest(
            chat_id=chat_id,
            user_id=user_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def delete_chat_photo(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = DeleteChatPhoto(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def delete_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = DeleteChatStickerSet(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def delete_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = DeleteForumTopic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def delete_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = DeleteMessage(
            chat_id=chat_id,
            message_id=message_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def delete_my_commands(
        self,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = DeleteMyCommands(
            scope=scope,
            language_code=language_code,
        )
        return await self.request(call, timeout=request_timeout)

    async def delete_sticker_from_set(
        self,
        sticker: str,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = DeleteStickerFromSet(
            sticker=sticker,
        )
        return await self.request(call, timeout=request_timeout)

    async def delete_webhook(
        self,
        drop_pending_updates: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = DeleteWebhook(
            drop_pending_updates=drop_pending_updates,
        )
        return await self.request(call, timeout=request_timeout)

    async def edit_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        name: Optional[str] = None,
        expire_date: Optional[Union[datetime.datetime, datetime.timedelta, int]] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> ChatInviteLink:
        call = EditChatInviteLink(
            chat_id=chat_id,
            invite_link=invite_link,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        )
        return await self.request(call, timeout=request_timeout)

    async def edit_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        name: Optional[str] = None,
        icon_custom_emoji_id: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = EditForumTopic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            name=name,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def edit_message_caption(
        self,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Union[Message, bool]:
        call = EditMessageCaption(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Union[Message, bool]:
        call = EditMessageLiveLocation(
            latitude=latitude,
            longitude=longitude,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            horizontal_accuracy=horizontal_accuracy,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def edit_message_media(
        self,
        media: InputMedia,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Union[Message, bool]:
        call = EditMessageMedia(
            media=media,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def edit_message_reply_markup(
        self,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Union[Message, bool]:
        call = EditMessageReplyMarkup(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def edit_message_text(
        self,
        text: str,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Union[Message, bool]:
        call = EditMessageText(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def export_chat_invite_link(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> str:
        call = ExportChatInviteLink(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = ForwardMessage(
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_chat(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> Chat:
        call = GetChat(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_chat_administrators(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> List[
        Union[
            ChatMemberOwner,
            ChatMemberAdministrator,
            ChatMemberMember,
            ChatMemberRestricted,
            ChatMemberLeft,
            ChatMemberBanned,
        ]
    ]:
        call = GetChatAdministrators(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        request_timeout: Optional[int] = None,
    ) -> Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ]:
        call = GetChatMember(
            chat_id=chat_id,
            user_id=user_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_chat_member_count(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> int:
        call = GetChatMemberCount(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_chat_menu_button(
        self,
        chat_id: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ) -> Union[MenuButtonDefault, MenuButtonWebApp, MenuButtonCommands]:
        call = GetChatMenuButton(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_custom_emoji_stickers(
        self,
        custom_emoji_ids: List[str],
        request_timeout: Optional[int] = None,
    ) -> List[Sticker]:
        call = GetCustomEmojiStickers(
            custom_emoji_ids=custom_emoji_ids,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_file(
        self,
        file_id: str,
        request_timeout: Optional[int] = None,
    ) -> File:
        call = GetFile(
            file_id=file_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_forum_topic_icon_stickers(
        self,
        request_timeout: Optional[int] = None,
    ) -> List[Sticker]:
        call = GetForumTopicIconStickers()
        return await self.request(call, timeout=request_timeout)

    async def get_game_high_scores(
        self,
        user_id: int,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> List[GameHighScore]:
        call = GetGameHighScores(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_me(
        self,
        request_timeout: Optional[int] = None,
    ) -> User:
        call = GetMe()
        return await self.request(call, timeout=request_timeout)

    async def get_my_commands(
        self,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> List[BotCommand]:
        call = GetMyCommands(
            scope=scope,
            language_code=language_code,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_my_default_administrator_rights(
        self,
        for_channels: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> ChatAdministratorRights:
        call = GetMyDefaultAdministratorRights(
            for_channels=for_channels,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_sticker_set(
        self,
        name: str,
        request_timeout: Optional[int] = None,
    ) -> StickerSet:
        call = GetStickerSet(
            name=name,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_updates(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None,
        request_timeout: Optional[int] = None,
    ) -> List[Update]:
        call = GetUpdates(
            offset=offset,
            limit=limit,
            timeout=timeout,
            allowed_updates=allowed_updates,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_user_profile_photos(
        self,
        user_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ) -> UserProfilePhotos:
        call = GetUserProfilePhotos(
            user_id=user_id,
            offset=offset,
            limit=limit,
        )
        return await self.request(call, timeout=request_timeout)

    async def get_webhook_info(
        self,
        request_timeout: Optional[int] = None,
    ) -> WebhookInfo:
        call = GetWebhookInfo()
        return await self.request(call, timeout=request_timeout)

    async def leave_chat(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = LeaveChat(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def log_out(
        self,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = LogOut()
        return await self.request(call, timeout=request_timeout)

    async def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        disable_notification: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = PinChatMessage(
            chat_id=chat_id,
            message_id=message_id,
            disable_notification=disable_notification,
        )
        return await self.request(call, timeout=request_timeout)

    async def promote_chat_member(
        self,
        chat_id: Union[int, str],
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
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = PromoteChatMember(
            chat_id=chat_id,
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
        )
        return await self.request(call, timeout=request_timeout)

    async def reopen_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = ReopenForumTopic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        permissions: ChatPermissions,
        until_date: Optional[Union[datetime.datetime, datetime.timedelta, int]] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = RestrictChatMember(
            chat_id=chat_id,
            user_id=user_id,
            permissions=permissions,
            until_date=until_date,
        )
        return await self.request(call, timeout=request_timeout)

    async def revoke_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        request_timeout: Optional[int] = None,
    ) -> ChatInviteLink:
        call = RevokeChatInviteLink(
            chat_id=chat_id,
            invite_link=invite_link,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_animation(
        self,
        chat_id: Union[int, str],
        animation: Union[InputFile, str],
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendAnimation(
            chat_id=chat_id,
            animation=animation,
            message_thread_id=message_thread_id,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_audio(
        self,
        chat_id: Union[int, str],
        audio: Union[InputFile, str],
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendAudio(
            chat_id=chat_id,
            audio=audio,
            message_thread_id=message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_chat_action(
        self,
        chat_id: Union[int, str],
        action: str,
        message_thread_id: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SendChatAction(
            chat_id=chat_id,
            action=action,
            message_thread_id=message_thread_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_contact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        message_thread_id: Optional[int] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendContact(
            chat_id=chat_id,
            phone_number=phone_number,
            first_name=first_name,
            message_thread_id=message_thread_id,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_dice(
        self,
        chat_id: Union[int, str],
        message_thread_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendDice(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[InputFile, str],
        message_thread_id: Optional[int] = None,
        thumb: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendDocument(
            chat_id=chat_id,
            document=document,
            message_thread_id=message_thread_id,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendGame(
            chat_id=chat_id,
            game_short_name=game_short_name,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_invoice(
        self,
        chat_id: Union[int, str],
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: List[LabeledPrice],
        message_thread_id: Optional[int] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendInvoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            message_thread_id=message_thread_id,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        message_thread_id: Optional[int] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendLocation(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            message_thread_id=message_thread_id,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_media_group(
        self,
        chat_id: Union[int, str],
        media: List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]],
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> List[Message]:
        call = SendMediaGroup(
            chat_id=chat_id,
            media=media,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        message_thread_id: Optional[int] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendMessage(
            chat_id=chat_id,
            text=text,
            message_thread_id=message_thread_id,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[InputFile, str],
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendPhoto(
            chat_id=chat_id,
            photo=photo,
            message_thread_id=message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        message_thread_id: Optional[int] = None,
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[Union[datetime.datetime, datetime.timedelta, int]] = None,
        is_closed: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendPoll(
            chat_id=chat_id,
            question=question,
            options=options,
            message_thread_id=message_thread_id,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_sticker(
        self,
        chat_id: Union[int, str],
        sticker: Union[InputFile, str],
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendSticker(
            chat_id=chat_id,
            sticker=sticker,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_venue(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        message_thread_id: Optional[int] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendVenue(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            message_thread_id=message_thread_id,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[InputFile, str],
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendVideo(
            chat_id=chat_id,
            video=video,
            message_thread_id=message_thread_id,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_video_note(
        self,
        chat_id: Union[int, str],
        video_note: Union[InputFile, str],
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumb: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendVideoNote(
            chat_id=chat_id,
            video_note=video_note,
            message_thread_id=message_thread_id,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def send_voice(
        self,
        chat_id: Union[int, str],
        voice: Union[InputFile, str],
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> Message:
        call = SendVoice(
            chat_id=chat_id,
            voice=voice,
            message_thread_id=message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_chat_administrator_custom_title(
        self,
        chat_id: Union[int, str],
        user_id: int,
        custom_title: str,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetChatAdministratorCustomTitle(
            chat_id=chat_id,
            user_id=user_id,
            custom_title=custom_title,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_chat_description(
        self,
        chat_id: Union[int, str],
        description: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetChatDescription(
            chat_id=chat_id,
            description=description,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_chat_menu_button(
        self,
        chat_id: Optional[int] = None,
        menu_button: Optional[
            Union[MenuButtonDefault, MenuButtonWebApp, MenuButtonCommands]
        ] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetChatMenuButton(
            chat_id=chat_id,
            menu_button=menu_button,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: ChatPermissions,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetChatPermissions(
            chat_id=chat_id,
            permissions=permissions,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo: InputFile,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetChatPhoto(
            chat_id=chat_id,
            photo=photo,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        sticker_set_name: str,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetChatStickerSet(
            chat_id=chat_id,
            sticker_set_name=sticker_set_name,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_chat_title(
        self,
        chat_id: Union[int, str],
        title: str,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetChatTitle(
            chat_id=chat_id,
            title=title,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_game_score(
        self,
        user_id: int,
        score: int,
        force: Optional[bool] = None,
        disable_edit_message: Optional[bool] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> Union[Message, bool]:
        call = SetGameScore(
            user_id=user_id,
            score=score,
            force=force,
            disable_edit_message=disable_edit_message,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_my_commands(
        self,
        commands: List[BotCommand],
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetMyCommands(
            commands=commands,
            scope=scope,
            language_code=language_code,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_my_default_administrator_rights(
        self,
        rights: Optional[ChatAdministratorRights] = None,
        for_channels: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetMyDefaultAdministratorRights(
            rights=rights,
            for_channels=for_channels,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_passport_data_errors(
        self,
        user_id: int,
        errors: List[PassportElementError],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetPassportDataErrors(
            user_id=user_id,
            errors=errors,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetStickerPositionInSet(
            sticker=sticker,
            position=position,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_sticker_set_thumb(
        self,
        name: str,
        user_id: int,
        thumb: Optional[Union[InputFile, str]] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetStickerSetThumb(
            name=name,
            user_id=user_id,
            thumb=thumb,
        )
        return await self.request(call, timeout=request_timeout)

    async def set_webhook(
        self,
        url: str,
        certificate: Optional[InputFile] = None,
        ip_address: Optional[str] = None,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None,
        drop_pending_updates: Optional[bool] = None,
        secret_token: Optional[str] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = SetWebhook(
            url=url,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
            secret_token=secret_token,
        )
        return await self.request(call, timeout=request_timeout)

    async def stop_message_live_location(
        self,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Union[Message, bool]:
        call = StopMessageLiveLocation(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def stop_poll(
        self,
        chat_id: Union[int, str],
        message_id: int,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        request_timeout: Optional[int] = None,
    ) -> Poll:
        call = StopPoll(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        )
        return await self.request(call, timeout=request_timeout)

    async def unban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        only_if_banned: Optional[bool] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = UnbanChatMember(
            chat_id=chat_id,
            user_id=user_id,
            only_if_banned=only_if_banned,
        )
        return await self.request(call, timeout=request_timeout)

    async def unban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = UnbanChatSenderChat(
            chat_id=chat_id,
            sender_chat_id=sender_chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def unpin_all_chat_messages(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = UnpinAllChatMessages(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def unpin_all_forum_topic_messages(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = UnpinAllForumTopicMessages(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def unpin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = UnpinChatMessage(
            chat_id=chat_id,
            message_id=message_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def upload_sticker_file(
        self,
        user_id: int,
        png_sticker: InputFile,
        request_timeout: Optional[int] = None,
    ) -> File:
        call = UploadStickerFile(
            user_id=user_id,
            png_sticker=png_sticker,
        )
        return await self.request(call, timeout=request_timeout)

    async def close_general_forum_topic(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = CloseGeneralForumTopic(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def edit_general_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = EditGeneralForumTopic(
            chat_id=chat_id,
            name=name,
        )
        return await self.request(call, timeout=request_timeout)

    async def hide_general_forum_topic(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = HideGeneralForumTopic(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def reopen_general_forum_topic(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = ReopenGeneralForumTopic(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)

    async def unhide_general_forum_topic(
        self,
        chat_id: Union[int, str],
        request_timeout: Optional[int] = None,
    ) -> bool:
        call = UnhideGeneralForumTopic(
            chat_id=chat_id,
        )
        return await self.request(call, timeout=request_timeout)
