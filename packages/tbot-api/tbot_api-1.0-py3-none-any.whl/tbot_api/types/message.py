from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from pydantic import Field

from ..enums import ContentType
from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import (
        CopyMessage,
        DeleteMessage,
        EditMessageCaption,
        EditMessageLiveLocation,
        EditMessageMedia,
        EditMessageReplyMarkup,
        EditMessageText,
        ForwardMessage,
        PinChatMessage,
        SendAnimation,
        SendAudio,
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
        StopMessageLiveLocation,
        UnpinChatMessage,
    )
    from .animation import Animation
    from .audio import Audio
    from .chat import Chat
    from .contact import Contact
    from .dice import Dice
    from .document import Document
    from .force_reply import ForceReply
    from .forum_topic_closed import ForumTopicClosed
    from .forum_topic_created import ForumTopicCreated
    from .forum_topic_reopened import ForumTopicReopened
    from .game import Game
    from .inline_keyboard_markup import InlineKeyboardMarkup
    from .input_file import InputFile
    from .input_media import InputMedia
    from .input_media_audio import InputMediaAudio
    from .input_media_document import InputMediaDocument
    from .input_media_photo import InputMediaPhoto
    from .input_media_video import InputMediaVideo
    from .invoice import Invoice
    from .labeled_price import LabeledPrice
    from .location import Location
    from .message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
    from .message_entity import MessageEntity
    from .passport_data import PassportData
    from .photo_size import PhotoSize
    from .poll import Poll
    from .proximity_alert_triggered import ProximityAlertTriggered
    from .reply_keyboard_markup import ReplyKeyboardMarkup
    from .reply_keyboard_remove import ReplyKeyboardRemove
    from .sticker import Sticker
    from .successful_payment import SuccessfulPayment
    from .user import User
    from .venue import Venue
    from .video import Video
    from .video_chat_ended import VideoChatEnded
    from .video_chat_participants_invited import VideoChatParticipantsInvited
    from .video_chat_scheduled import VideoChatScheduled
    from .video_chat_started import VideoChatStarted
    from .video_note import VideoNote
    from .voice import Voice
    from .web_app_data import WebAppData


class Message(TelegramObject):
    message_id: int
    message_thread_id: Optional[int] = None
    date: datetime
    chat: Chat
    from_user: Optional[User] = Field(None, alias="from")
    sender_chat: Optional[Chat] = None
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[int] = None
    is_topic_message: Optional[bool] = None
    is_automatic_forward: Optional[bool] = None
    reply_to_message: Optional[Message] = None
    via_bot: Optional[User] = None
    edit_date: Optional[int] = None
    has_protected_content: Optional[bool] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    photo: Optional[List[PhotoSize]] = None
    sticker: Optional[Sticker] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[Game] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
    location: Optional[Location] = None
    new_chat_members: Optional[List[User]] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[List[PhotoSize]] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional[Message] = None
    invoice: Optional[Invoice] = None
    successful_payment: Optional[SuccessfulPayment] = None
    connected_website: Optional[str] = None
    passport_data: Optional[PassportData] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    forum_topic_created: Optional[ForumTopicCreated] = None
    forum_topic_closed: Optional[ForumTopicClosed] = None
    forum_topic_reopened: Optional[ForumTopicReopened] = None
    video_chat_scheduled: Optional[VideoChatScheduled] = None
    video_chat_started: Optional[VideoChatStarted] = None
    video_chat_ended: Optional[VideoChatEnded] = None
    video_chat_participants_invited: Optional[VideoChatParticipantsInvited] = None
    web_app_data: Optional[WebAppData] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None

    @property
    def content_type(self) -> str:
        if self.text:
            return ContentType.TEXT
        if self.audio:
            return ContentType.AUDIO
        if self.animation:
            return ContentType.ANIMATION
        if self.document:
            return ContentType.DOCUMENT
        if self.game:
            return ContentType.GAME
        if self.photo:
            return ContentType.PHOTO
        if self.sticker:
            return ContentType.STICKER
        if self.video:
            return ContentType.VIDEO
        if self.video_note:
            return ContentType.VIDEO_NOTE
        if self.voice:
            return ContentType.VOICE
        if self.contact:
            return ContentType.CONTACT
        if self.venue:
            return ContentType.VENUE
        if self.location:
            return ContentType.LOCATION
        if self.new_chat_members:
            return ContentType.NEW_CHAT_MEMBERS
        if self.left_chat_member:
            return ContentType.LEFT_CHAT_MEMBER
        if self.invoice:
            return ContentType.INVOICE
        if self.successful_payment:
            return ContentType.SUCCESSFUL_PAYMENT
        if self.connected_website:
            return ContentType.CONNECTED_WEBSITE
        if self.migrate_from_chat_id:
            return ContentType.MIGRATE_FROM_CHAT_ID
        if self.migrate_to_chat_id:
            return ContentType.MIGRATE_TO_CHAT_ID
        if self.pinned_message:
            return ContentType.PINNED_MESSAGE
        if self.new_chat_title:
            return ContentType.NEW_CHAT_TITLE
        if self.new_chat_photo:
            return ContentType.NEW_CHAT_PHOTO
        if self.delete_chat_photo:
            return ContentType.DELETE_CHAT_PHOTO
        if self.group_chat_created:
            return ContentType.GROUP_CHAT_CREATED
        if self.supergroup_chat_created:
            return ContentType.SUPERGROUP_CHAT_CREATED
        if self.channel_chat_created:
            return ContentType.CHANNEL_CHAT_CREATED
        if self.passport_data:
            return ContentType.PASSPORT_DATA
        if self.proximity_alert_triggered:
            return ContentType.PROXIMITY_ALERT_TRIGGERED
        if self.poll:
            return ContentType.POLL
        if self.dice:
            return ContentType.DICE
        if self.message_auto_delete_timer_changed:
            return ContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED
        if self.forum_topic_created:
            return ContentType.FORUM_TOPIC_CREATED
        if self.forum_topic_closed:
            return ContentType.FORUM_TOPIC_CLOSED
        if self.forum_topic_reopened:
            return ContentType.FORUM_TOPIC_REOPENED
        if self.video_chat_scheduled:
            return ContentType.VIDEO_CHAT_SCHEDULED
        if self.video_chat_started:
            return ContentType.VIDEO_CHAT_STARTED
        if self.video_chat_ended:
            return ContentType.VIDEO_CHAT_ENDED
        if self.video_chat_participants_invited:
            return ContentType.VIDEO_CHAT_PARTICIPANTS_INVITED
        if self.web_app_data:
            return ContentType.WEB_APP_DATA

        return ContentType.UNKNOWN

    def reply_animation(
        self,
        animation: Union[str, InputFile],
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[str, InputFile]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendAnimation:
        from ..methods import SendAnimation

        return SendAnimation(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            animation=animation,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_animation(
        self,
        animation: Union[str, InputFile],
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[str, InputFile]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendAnimation:
        from ..methods import SendAnimation

        return SendAnimation(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            animation=animation,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_audio(
        self,
        audio: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Optional[Union[str, InputFile]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendAudio:
        from ..methods import SendAudio

        return SendAudio(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_audio(
        self,
        audio: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Optional[Union[str, InputFile]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendAudio:
        from ..methods import SendAudio

        return SendAudio(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            audio=audio,
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
            **kwargs,
        )

    def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendContact:
        from ..methods import SendContact

        return SendContact(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_contact(
        self,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendContact:
        from ..methods import SendContact

        return SendContact(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_document(
        self,
        document: Union[str, InputFile],
        thumb: Optional[Union[str, InputFile]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendDocument:
        from ..methods import SendDocument

        return SendDocument(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            document=document,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_document(
        self,
        document: Union[str, InputFile],
        thumb: Optional[Union[str, InputFile]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendDocument:
        from ..methods import SendDocument

        return SendDocument(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            document=document,
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
            **kwargs,
        )

    def reply_game(
        self,
        game_short_name: str,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> SendGame:
        from ..methods import SendGame

        return SendGame(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_game(
        self,
        game_short_name: str,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> SendGame:
        from ..methods import SendGame

        return SendGame(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_invoice(
        self,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: List[LabeledPrice],
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
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> SendInvoice:
        from ..methods import SendInvoice

        return SendInvoice(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
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
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_invoice(
        self,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: List[LabeledPrice],
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
        **kwargs: Dict,
    ) -> SendInvoice:
        from ..methods import SendInvoice

        return SendInvoice(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
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
            **kwargs,
        )

    def reply_location(
        self,
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendLocation:
        from ..methods import SendLocation

        return SendLocation(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_location(
        self,
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendLocation:
        from ..methods import SendLocation

        return SendLocation(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_media_group(
        self,
        media: List[
            Union[
                InputMediaAudio,
                InputMediaDocument,
                InputMediaPhoto,
                InputMediaVideo,
            ]
        ],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        **kwargs: Dict,
    ) -> SendMediaGroup:
        from ..methods import SendMediaGroup

        return SendMediaGroup(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            **kwargs,
        )

    def answer_media_group(
        self,
        media: List[
            Union[
                InputMediaAudio,
                InputMediaDocument,
                InputMediaPhoto,
                InputMediaVideo,
            ]
        ],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        **kwargs: Dict,
    ) -> SendMediaGroup:
        from ..methods import SendMediaGroup

        return SendMediaGroup(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            **kwargs,
        )

    def reply(
        self,
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendMessage:
        from ..methods import SendMessage

        return SendMessage(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer(
        self,
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendMessage:
        from ..methods import SendMessage

        return SendMessage(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_photo(
        self,
        photo: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendPhoto:
        from ..methods import SendPhoto

        return SendPhoto(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_photo(
        self,
        photo: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendPhoto:
        from ..methods import SendPhoto

        return SendPhoto(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_poll(
        self,
        question: str,
        options: List[str],
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[Union[int, datetime, timedelta]] = None,
        is_closed: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendPoll:
        from ..methods import SendPoll

        return SendPoll(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            question=question,
            options=options,
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
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_poll(
        self,
        question: str,
        options: List[str],
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[Union[int, datetime, timedelta]] = None,
        is_closed: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendPoll:
        from ..methods import SendPoll

        return SendPoll(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            question=question,
            options=options,
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
            **kwargs,
        )

    def reply_dice(
        self,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendDice:
        from ..methods import SendDice

        return SendDice(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_dice(
        self,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendDice:
        from ..methods import SendDice

        return SendDice(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_sticker(
        self,
        sticker: Union[str, InputFile],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendSticker:
        from ..methods import SendSticker

        return SendSticker(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            sticker=sticker,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_sticker(
        self,
        sticker: Union[str, InputFile],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendSticker:
        from ..methods import SendSticker

        return SendSticker(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            sticker=sticker,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendVenue:
        from ..methods import SendVenue

        return SendVenue(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendVenue:
        from ..methods import SendVenue

        return SendVenue(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_video(
        self,
        video: Union[str, InputFile],
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[str, InputFile]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendVideo:
        from ..methods import SendVideo

        return SendVideo(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_video(
        self,
        video: Union[str, InputFile],
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[str, InputFile]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendVideo:
        from ..methods import SendVideo

        return SendVideo(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_video_note(
        self,
        video_note: Union[str, InputFile],
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumb: Optional[Union[str, InputFile]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendVideoNote:
        from ..methods import SendVideoNote

        return SendVideoNote(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_video_note(
        self,
        video_note: Union[str, InputFile],
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumb: Optional[Union[str, InputFile]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendVideoNote:
        from ..methods import SendVideoNote

        return SendVideoNote(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def reply_voice(
        self,
        voice: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendVoice:
        from ..methods import SendVoice

        return SendVoice(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            reply_to_message_id=self.message_id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def answer_voice(
        self,
        voice: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> SendVoice:
        from ..methods import SendVoice

        return SendVoice(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id if self.is_topic_message else None,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def send_copy(
        self: Message,
        chat_id: Union[str, int],
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, None] = None,
        allow_sending_without_reply: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
    ) -> Union[
        SendAnimation,
        SendAudio,
        SendContact,
        SendDocument,
        SendLocation,
        SendMessage,
        SendPhoto,
        SendPoll,
        SendDice,
        SendSticker,
        SendVenue,
        SendVideo,
        SendVideoNote,
        SendVoice,
    ]:
        from ..methods import (
            SendAnimation,
            SendAudio,
            SendContact,
            SendDice,
            SendDocument,
            SendLocation,
            SendMessage,
            SendPhoto,
            SendPoll,
            SendSticker,
            SendVenue,
            SendVideo,
            SendVideoNote,
            SendVoice,
        )

        kwargs = {
            "chat_id": chat_id,
            "reply_markup": reply_markup or self.reply_markup,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "message_thread_id": message_thread_id,
            "allow_sending_without_reply": allow_sending_without_reply,
        }
        text = self.text or self.caption
        entities = self.entities or self.caption_entities

        if self.text:
            return SendMessage(text=text, entities=entities, **kwargs)
        if self.audio:
            return SendAudio(
                audio=self.audio.file_id,
                caption=text,
                title=self.audio.title,
                performer=self.audio.performer,
                duration=self.audio.duration,
                caption_entities=entities,
                **kwargs,
            )
        if self.animation:
            return SendAnimation(
                animation=self.animation.file_id, caption=text, caption_entities=entities, **kwargs
            )
        if self.document:
            return SendDocument(
                document=self.document.file_id, caption=text, caption_entities=entities, **kwargs
            )
        if self.photo:
            return SendPhoto(
                photo=self.photo[-1].file_id, caption=text, caption_entities=entities, **kwargs
            )
        if self.sticker:
            return SendSticker(sticker=self.sticker.file_id, **kwargs)
        if self.video:
            return SendVideo(
                video=self.video.file_id, caption=text, caption_entities=entities, **kwargs
            )
        if self.video_note:
            return SendVideoNote(video_note=self.video_note.file_id, **kwargs)
        if self.voice:
            return SendVoice(voice=self.voice.file_id, **kwargs)
        if self.contact:
            return SendContact(
                phone_number=self.contact.phone_number,
                first_name=self.contact.first_name,
                last_name=self.contact.last_name,
                vcard=self.contact.vcard,
                **kwargs,
            )
        if self.venue:
            return SendVenue(
                latitude=self.venue.location.latitude,
                longitude=self.venue.location.longitude,
                title=self.venue.title,
                address=self.venue.address,
                foursquare_id=self.venue.foursquare_id,
                foursquare_type=self.venue.foursquare_type,
                **kwargs,
            )
        if self.location:
            return SendLocation(
                latitude=self.location.latitude, longitude=self.location.longitude, **kwargs
            )
        if self.poll:
            return SendPoll(
                question=self.poll.question,
                options=[option.text for option in self.poll.options],
                **kwargs,
            )
        if self.dice:
            return SendDice(**kwargs)
        raise TypeError("This type of message can't be copied.")

    def copy_to(
        self,
        chat_id: Union[int, str],
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
        **kwargs: Dict,
    ) -> CopyMessage:
        from ..methods import CopyMessage

        return CopyMessage(
            from_chat_id=self.chat.id,
            message_id=self.message_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            **kwargs,
        )

    def edit_text(
        self,
        text: str,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> EditMessageText:
        from ..methods import EditMessageText

        return EditMessageText(
            chat_id=self.chat.id,
            message_id=self.message_id,
            text=text,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
            **kwargs,
        )

    def forward(
        self,
        chat_id: Union[int, str],
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        **kwargs: Dict,
    ) -> ForwardMessage:
        from ..methods import ForwardMessage

        return ForwardMessage(
            from_chat_id=self.chat.id,
            message_id=self.message_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            **kwargs,
        )

    def edit_media(
        self,
        media: InputMedia,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> EditMessageMedia:
        from ..methods import EditMessageMedia

        return EditMessageMedia(
            chat_id=self.chat.id,
            message_id=self.message_id,
            media=media,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
            **kwargs,
        )

    def edit_reply_markup(
        self,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> EditMessageReplyMarkup:
        from ..methods import EditMessageReplyMarkup

        return EditMessageReplyMarkup(
            chat_id=self.chat.id,
            message_id=self.message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
            **kwargs,
        )

    def delete_reply_markup(self) -> EditMessageReplyMarkup:
        return self.edit_reply_markup(reply_markup=None)

    def edit_live_location(
        self,
        latitude: float,
        longitude: float,
        inline_message_id: Optional[str] = None,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> EditMessageLiveLocation:
        from ..methods import EditMessageLiveLocation

        return EditMessageLiveLocation(
            chat_id=self.chat.id,
            message_id=self.message_id,
            latitude=latitude,
            longitude=longitude,
            inline_message_id=inline_message_id,
            horizontal_accuracy=horizontal_accuracy,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            reply_markup=reply_markup,
            **kwargs,
        )

    def stop_live_location(
        self,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> StopMessageLiveLocation:
        from ..methods import StopMessageLiveLocation

        return StopMessageLiveLocation(
            chat_id=self.chat.id,
            message_id=self.message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
            **kwargs,
        )

    def edit_caption(
        self,
        inline_message_id: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Dict,
    ) -> EditMessageCaption:
        from ..methods import EditMessageCaption

        return EditMessageCaption(
            chat_id=self.chat.id,
            message_id=self.message_id,
            inline_message_id=inline_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup,
            **kwargs,
        )

    def delete(
        self,
        **kwargs: Dict,
    ) -> DeleteMessage:
        from ..methods import DeleteMessage

        return DeleteMessage(
            chat_id=self.chat.id,
            message_id=self.message_id,
            **kwargs,
        )

    def pin(
        self,
        disable_notification: Optional[bool] = None,
        **kwargs: Dict,
    ) -> PinChatMessage:
        from ..methods import PinChatMessage

        return PinChatMessage(
            chat_id=self.chat.id,
            message_id=self.message_id,
            disable_notification=disable_notification,
            **kwargs,
        )

    def unpin(
        self,
        **kwargs: Dict,
    ) -> UnpinChatMessage:
        from ..methods import UnpinChatMessage

        return UnpinChatMessage(
            chat_id=self.chat.id,
            message_id=self.message_id,
            **kwargs,
        )
