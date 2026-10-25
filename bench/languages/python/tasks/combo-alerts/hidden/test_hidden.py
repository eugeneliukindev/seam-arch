"""Hidden checks for combo-alerts: three channels deliver, and after two edits no shared unit branches on the channel."""

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


def test_gate_sms_without_phone_falls_back_to_mail() -> None:
    service, smtp, sms, push = _service()
    service.alert(User(id=3, email="c@example.com", phone=None, device_token=None, channel="sms"), "disk full")
    assert smtp.sent == ["c@example.com"]


def _contracts():
    found = {}
    for path in Path("alerts").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ClassDef):
                bases = {ast.unparse(b).split(".")[-1].split("[")[0] for b in node.bases}
                if bases & {"ABC", "Protocol"}:
                    found[node.name] = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
    return found


def test_design_notifier_contract_is_narrow() -> None:
    wide = {name: methods for name, methods in _contracts().items() if len(methods) > 1}
    assert not wide, f"a contract that asks for more than delivering one alert: {wide}"


def test_design_every_notifier_honours_the_contract() -> None:
    import inspect
    import importlib

    for path in Path("alerts").glob("*.py"):
        module = importlib.import_module(f"alerts.{path.stem}")
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ == module.__name__ and cls.__name__.endswith("Notifier") and not inspect.isabstract(cls):
                source = inspect.getsource(cls)
                assert "NotImplementedError" not in source, f"{cls.__name__} refuses part of the contract"
