from alerts.app import build_service
from alerts.gateways import PushGateway, SmsGateway, SmtpClient
from alerts.users import User


class FakeSmtp(SmtpClient):
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send_mail(self, to: str, subject: str, body: str) -> None:
        self.sent.append((to, body))


def test_alert_by_mail() -> None:
    smtp = FakeSmtp()
    service = build_service(smtp, SmsGateway(), PushGateway())
    service.alert(User(id=1, email="a@example.com"), "disk full")
    assert smtp.sent == [("a@example.com", "disk full")]
