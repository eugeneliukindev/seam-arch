"""Alerts delivered to the phone app."""

from __future__ import annotations

from alerts.gateways import PushGateway
from alerts.service import Notifier
from alerts.users import User


class PushNotifier(Notifier):
    """Delivers an alert to a user's phone app, or by the fallback when there is no device."""

    def __init__(self, gateway: PushGateway, *, fallback: Notifier) -> None:
        self._gateway = gateway
        self._fallback = fallback

    def notify(self, user: User, text: str) -> None:
        """Push `text` to `user`'s app."""
        if user.device_token is None:
            self._fallback.notify(user, text)
            return
        self._gateway.send(user.device_token, text)
