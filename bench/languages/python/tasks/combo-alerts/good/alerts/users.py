"""The people alerts go to."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

type Channel = Literal["email", "sms", "push"]


@dataclass(frozen=True, slots=True, kw_only=True)
class User:
    """A user who receives alerts."""

    id: int
    email: str
    phone: str | None = None
    device_token: str | None = None
    channel: Channel = "email"
