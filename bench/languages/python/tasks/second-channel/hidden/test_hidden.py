"""Hidden checks for second-channel: three channels deliver, and after two edits no shared unit branches on the channel."""

import ast
from pathlib import Path

from alerts.gateways import PushGateway, SmsGateway, SmtpClient
from alerts.users import User


class FakeSmtp(SmtpClient):
    def __init__(self) -> None:
        self.sent: list[str] = []

    def send_mail(self, to: str, subject: str, body: str) -> None:
        self.sent.append(to)


class FakeSms(SmsGateway):
    def __init__(self) -> None:
        self.sent: list[str] = []

    def send(self, phone: str, text: str) -> None:
        self.sent.append(phone)


class FakePush(PushGateway):
    def __init__(self) -> None:
        self.sent: list[str] = []

    def send(self, device_token: str, text: str) -> None:
        self.sent.append(device_token)


def _service():
    from alerts.app import build_service

    smtp, sms, push = FakeSmtp(), FakeSms(), FakePush()
    return build_service(smtp, sms, push), smtp, sms, push


def _user(channel: str) -> User:
    return User(id=1, email="a@example.com", phone="+100", device_token="dev-1", channel=channel)


def test_gate_each_channel_delivers() -> None:
    for channel, pick in (("email", 1), ("sms", 2), ("push", 3)):
        service, *sinks = _service()
        service.alert(_user(channel), "disk full")
        assert [len(sink.sent) for sink in sinks] == [int(i == pick) for i in (1, 2, 3)], channel


def _compares_channel_names(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = {"sms", "email", "push", "SMS", "EMAIL", "PUSH"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for side in [node.left, *node.comparators]:
                if isinstance(side, ast.Constant) and side.value in names:
                    return True
                if isinstance(side, ast.Attribute) and side.attr in names:
                    return True
        if isinstance(node, ast.match_case) and any(n in ast.unparse(node.pattern).lower() for n in ("sms", "push")):
            return True
    return False


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    assert not _compares_channel_names(Path("alerts/service.py"))


def test_design_each_notifier_knows_only_its_channel() -> None:
    assert "sms" not in Path("alerts/email.py").read_text(encoding="utf-8").lower()
    assert "push" not in Path("alerts/email.py").read_text(encoding="utf-8").lower()
    sms = Path("alerts/sms.py")
    assert not sms.exists() or "push" not in sms.read_text(encoding="utf-8").lower()
