"""Alerts delivered by text message."""

from __future__ import annotations

from alerts.gateways import SmsGateway
from alerts.service import Notifier
from alerts.users import User


class SmsNotifier(Notifier):
    """Delivers an alert to a user's phone, or by the fallback when there is no phone."""

    def __init__(self, gateway: SmsGateway, *, fallback: Notifier) -> None:
        self._gateway = gateway
        self._fallback = fallback

    def notify(self, user: User, text: str) -> None:
        """Text `text` to `user`."""
        if user.phone is None:
            self._fallback.notify(user, text)
            return
        self._gateway.send(user.phone, text)
