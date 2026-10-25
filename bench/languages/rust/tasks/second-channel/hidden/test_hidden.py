"""Hidden checks for second-channel: three channels deliver, and after two edits no shared unit branches on the channel."""

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


def test_gate_each_channel_delivers() -> None:
    _cargo_test("each_channel")


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    found = re.findall(r"\b(?:Sms|Email|Push|SMS|EMAIL|PUSH)\b|\"(?i:sms|email|push)\"", _code(Path("src/service.rs")))
    assert not found, f"src/service.rs names channels: {sorted(set(found))}"


def test_design_each_notifier_knows_only_its_channel() -> None:
    email = _code(Path("src/email.rs")).lower()
    assert "sms" not in email and "push" not in email, "src/email.rs knows of other channels"
    assert "push" not in _code(Path("src/sms.rs")).lower(), "src/sms.rs knows of push"
