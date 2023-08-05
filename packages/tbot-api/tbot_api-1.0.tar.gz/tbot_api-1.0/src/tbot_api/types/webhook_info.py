from __future__ import annotations

import datetime
from typing import List, Optional

from .base import TelegramObject


class WebhookInfo(TelegramObject):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str] = None
    last_error_date: Optional[datetime.datetime] = None
    last_error_message: Optional[str] = None
    last_synchronization_error_date: Optional[datetime.datetime] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = None
