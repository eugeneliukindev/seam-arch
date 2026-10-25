"""Hidden checks for notify-channel: SMS works, and no shared unit branches on the channel name."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent
# the gateways the seed already has: interfaces of the delivery clients, not of the notifiers
GATEWAYS = {"SmtpClient", "SmsGateway"}


def _go_test(name: str) -> None:
    target = Path("zz_hidden_checks_test.go")
    shutil.copy(HIDDEN / "hidden_test.go", target)
    try:
        completed = subprocess.run(
            ["go", "test", "-count=1", "-run", f"^{name}$", "./..."], capture_output=True, text=True, check=False
        )
    finally:
        target.unlink()
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _code(path: Path) -> str:
    """The Go source of `path` without its comments."""
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


def _sources() -> list[Path]:
    return [path for path in Path().glob("*.go") if not path.name.endswith("_test.go")]


def test_gate_sms_user_gets_a_text() -> None:
    _go_test("TestHiddenSmsUserGetsAText")


def test_gate_email_user_gets_mail() -> None:
    _go_test("TestHiddenEmailUserGetsMail")


def test_design_mail_notifier_knows_nothing_of_sms() -> None:
    assert "sms" not in Path("email.go").read_text(encoding="utf-8").lower()


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    code = _code(Path("service.go"))
    name = r"[\w.\"]*(?:sms|email)[\w.\"]*"
    branch = re.compile(rf"(?:==|!=|\bcase)\s*{name}|{name}\s*(?:==|!=)|\bswitch\s+[\w.]*\.Channel\b", re.IGNORECASE)
    found = branch.findall(code)
    assert not found, f"service.go branches on the channel name: {found}"


def test_design_notifiers_share_an_interface() -> None:
    found = {name for path in _sources() for name in re.findall(r"\btype\s+(\w+)\s+interface\b", _code(path))}
    assert found - GATEWAYS, "no interface the notifiers share"
