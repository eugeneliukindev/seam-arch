"""Hidden checks for second-channel: three channels deliver, and after two edits no shared unit branches on the channel."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent


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


def test_gate_each_channel_delivers() -> None:
    _go_test("TestHiddenEachChannelDelivers")


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    code = _code(Path("service.go"))
    name = r"[\w.\"]*(?:sms|email|push)[\w.\"]*"
    branch = re.compile(rf"(?:==|!=|\bcase)\s*{name}|{name}\s*(?:==|!=)|\bswitch\s+[\w.]*\.Channel\b", re.IGNORECASE)
    found = branch.findall(code)
    assert not found, f"service.go branches on the channel name: {found}"


def test_design_each_notifier_knows_only_its_channel() -> None:
    email = Path("email.go").read_text(encoding="utf-8").lower()
    assert "sms" not in email, "email.go knows of text messages"
    assert "push" not in email, "email.go knows of push notifications"
    sms = Path("sms.go")
    assert not sms.exists() or "push" not in sms.read_text(encoding="utf-8").lower(), "sms.go knows of push notifications"
