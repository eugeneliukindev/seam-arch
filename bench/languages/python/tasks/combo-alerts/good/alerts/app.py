"""Builds the alert service from the delivery clients."""

from __future__ import annotations

from alerts.email import EmailNotifier
from alerts.gateways import PushGateway, SmsGateway, SmtpClient
from alerts.push import PushNotifier
from alerts.service import AlertService
from alerts.sms import SmsNotifier


def build_service(smtp: SmtpClient, sms: SmsGateway, push: PushGateway) -> AlertService:
    """The alert service the application uses."""
    email = EmailNotifier(smtp)
    notifiers = {
        "email": email,
        "sms": SmsNotifier(sms, fallback=email),
        "push": PushNotifier(push, fallback=email),
    }
    return AlertService(notifiers)
