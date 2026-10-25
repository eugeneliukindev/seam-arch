"""Hidden checks for notify-channel: SMS works, and no shared unit branches on the channel name."""

import re
import subprocess
from pathlib import Path

import pytest

HIDDEN = Path(__file__).parent


def _code(path: Path) -> str:
    """The Java source in `path` without its comments."""
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


@pytest.fixture(scope="module")
def build(tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("build")
    sources = sorted(str(path) for path in Path("src").rglob("*.java"))
    compiled = subprocess.run(
        ["javac", "-d", str(directory), *sources, str(HIDDEN / "HiddenChecks.java")],
        capture_output=True, text=True, check=False,
    )
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    return directory


def _check(build: Path, name: str) -> None:
    ran = subprocess.run(
        ["java", "-cp", str(build), "HiddenChecks", name], capture_output=True, text=True, timeout=60, check=False
    )
    assert ran.returncode == 0, ran.stdout + ran.stderr


_NAME = r"(?:\w+\s*\.\s*)?(?:SMS|EMAIL|\"sms\"|\"email\")"
_BRANCHES = (
    rf"(?:==|!=)\s*{_NAME}\b",
    rf"\b{_NAME}\s*(?:==|!=)",
    rf"\.\s*equals(?:IgnoreCase)?\s*\(\s*{_NAME}",
    rf"{_NAME}\s*\.\s*equals",
    rf"\bcase\s+{_NAME}",
    r"\bswitch\s*\([^)]*channel",
)


def test_gate_sms_user_gets_a_text(build: Path) -> None:
    _check(build, "sms")


def test_gate_email_user_gets_mail(build: Path) -> None:
    _check(build, "email")


def test_design_mail_notifier_knows_nothing_of_sms() -> None:
    assert "sms" not in Path("src/alerts/EmailNotifier.java").read_text(encoding="utf-8").lower()


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    code = _code(Path("src/alerts/AlertService.java"))
    found = [pattern for pattern in _BRANCHES if re.search(pattern, code, flags=re.IGNORECASE)]
    assert not found, f"the service branches on the channel: {found}"


def test_design_notifiers_share_an_abstract_type() -> None:
    found = [
        name
        for path in Path("src/alerts").glob("*.java")
        for name in re.findall(r"\b(?:interface|abstract\s+class)\s+(\w+)", _code(path))
    ]
    assert found, "no abstract type the notifiers share"
