"""Alerts delivered to the phone app."""

from __future__ import annotations

from alerts.gateways import PushGateway
from alerts.service import Notifier
from alerts.users import User


class PushNotifier(Notifier):
    """Delivers an alert to a user's phone app."""

    def __init__(self, gateway: PushGateway) -> None:
        self._gateway = gateway

    def notify(self, user: User, text: str) -> None:
        """Push `text` to `user`'s app."""
        if user.device_token is None:
            raise ValueError(f"user {user.id} chose push but has no device")
        self._gateway.send(user.device_token, text)
