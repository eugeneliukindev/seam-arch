"""Raising alerts."""

from __future__ import annotations

from alerts.email import EmailNotifier
from alerts.gateways import PushGateway, SmsGateway
from alerts.users import User


class AlertService:
    """Raises alerts for users."""

    def __init__(self, notifier: EmailNotifier, sms: SmsGateway, push: PushGateway) -> None:
        self._notifier = notifier
        self._sms = sms
        self._push = push

    def alert(self, user: User, text: str) -> None:
        """Deliver `text` to `user`."""
        if user.channel == "sms" and user.phone:
            self._sms.send(user.phone, text)
        elif user.channel == "push" and user.device_token:
            self._push.send(user.device_token, text)
        else:
            self._notifier.notify(user, text)
