from __future__ import annotations

from typing import Optional

from .base import TelegramObject


class Location(TelegramObject):
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
