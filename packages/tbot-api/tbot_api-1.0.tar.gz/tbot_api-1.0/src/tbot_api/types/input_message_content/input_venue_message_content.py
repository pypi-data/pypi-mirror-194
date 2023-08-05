from __future__ import annotations

from typing import Optional

from .input_message_content import InputMessageContent


class InputVenueMessageContent(InputMessageContent):
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
