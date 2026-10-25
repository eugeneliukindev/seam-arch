"""Hidden checks for notify-channel: SMS works, and no shared unit branches on the channel name."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent


def _cargo_test(name: str) -> None:
    """Run the hidden integration test `name`.rs against the workspace crate."""
    target = f"hidden_{name}"
    Path("tests").mkdir(exist_ok=True)
    shutil.copy(HIDDEN / f"{name}.rs", Path("tests") / f"{target}.rs")
    completed = subprocess.run(
        ["cargo", "test", "--offline", "--quiet", "--test", target], capture_output=True, text=True, check=False
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _code(path: Path) -> str:
    """The Rust source of `path` without comments; empty when the file does not exist."""
    if not path.exists():
        return ""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


def _traits() -> set[str]:
    """Names of the traits the crate declares."""
    return {name for path in Path("src").rglob("*.rs") for name in re.findall(r"\btrait\s+(\w+)", _code(path))}



def test_gate_sms_user_gets_a_text() -> None:
    _cargo_test("sms_user")


def test_gate_email_user_gets_mail() -> None:
    _cargo_test("email_user")


def test_design_mail_notifier_knows_nothing_of_sms() -> None:
    assert "sms" not in _code(Path("src/email.rs")).lower()


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    found = re.findall(r"\b(?:Sms|Email|SMS|EMAIL)\b|\"(?i:sms|email)\"", _code(Path("src/service.rs")))
    assert not found, f"src/service.rs names channels: {sorted(set(found))}"


def test_design_notifiers_share_an_abstract_type() -> None:
    shared = _traits() - {"SmtpClient", "SmsGateway"}
    assert shared, "no trait the notifiers share"
