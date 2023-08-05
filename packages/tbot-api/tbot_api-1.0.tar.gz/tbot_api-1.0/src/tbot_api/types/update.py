from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from ..enums import UpdateType
from .base import TelegramObject

if TYPE_CHECKING:
    from .callback_query import CallbackQuery
    from .chat_join_request import ChatJoinRequest
    from .chat_member_updated import ChatMemberUpdated
    from .chosen_inline_result import ChosenInlineResult
    from .inline_query import InlineQuery
    from .message import Message
    from .poll import Poll
    from .poll_answer import PollAnswer
    from .pre_checkout_query import PreCheckoutQuery
    from .shipping_query import ShippingQuery


class Update(TelegramObject):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None
    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None
    my_chat_member: Optional[ChatMemberUpdated] = None
    chat_member: Optional[ChatMemberUpdated] = None
    chat_join_request: Optional[ChatJoinRequest] = None

    def __hash__(self) -> int:
        return hash((type(self), self.update_id))

    @property
    def type(self) -> str:
        if self.message:
            return UpdateType.MESSAGE
        if self.edited_message:
            return UpdateType.EDITED_MESSAGE
        if self.channel_post:
            return UpdateType.CHANNEL_POST
        if self.edited_channel_post:
            return UpdateType.EDITED_MESSAGE
        if self.inline_query:
            return UpdateType.INLINE_QUERY
        if self.chosen_inline_result:
            return UpdateType.CHOSEN_INLINE_RESULT
        if self.callback_query:
            return UpdateType.CALLBACK_QUERY
        if self.shipping_query:
            return UpdateType.SHIPPING_QUERY
        if self.pre_checkout_query:
            return UpdateType.PRE_CHECKOUT_QUERY
        if self.poll:
            return UpdateType.POLL
        if self.poll_answer:
            return UpdateType.POLL_ANSWER
        if self.my_chat_member:
            return UpdateType.MY_CHAT_MEMBER
        if self.chat_member:
            return UpdateType.CHAT_MEMBER
        if self.chat_join_request:
            return UpdateType.CHAT_JOIN_REQUEST
        return UpdateType.UNKNOWN

    @property
    def update(self) -> TelegramObject:
        _type = self.type
        return cast(TelegramObject, getattr(self, _type))
