"""Hidden checks for notify-channel: SMS works, and no shared unit branches on the channel name."""

import re
import subprocess
from functools import cache
from pathlib import Path

_CHECK = Path(__file__).parent / "Check"


@cache
def _check_output() -> str:
    """What the check program prints: one `PASS <scenario>` or `FAIL <scenario>: <why>` per line."""
    completed = subprocess.run(
        ["dotnet", "run", "--project", str(_CHECK)], capture_output=True, text=True, check=False
    )
    return completed.stdout + completed.stderr


def _assert_passes(scenario: str) -> None:
    assert f"PASS {scenario}" in _check_output().splitlines(), _check_output()


def _source(path: Path) -> str:
    """C# source without its comments."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


def _sources(directory: str) -> dict[Path, str]:
    return {
        path: _source(path)
        for path in Path(directory).rglob("*.cs")
        if not {"bin", "obj"} & set(path.parts)
    }


def _abstract_types(directory: str) -> list[str]:
    """Interfaces and abstract classes declared under `directory`."""
    pattern = re.compile(r"\binterface\s+(\w+)|\babstract\s+(?:partial\s+)?(?:class|record)\s+(\w+)")
    return [
        first or second
        for text in _sources(directory).values()
        for first, second in pattern.findall(text)
    ]


def test_gate_sms_user_gets_a_text() -> None:
    _assert_passes("sms user gets a text")


def test_gate_email_user_gets_mail() -> None:
    _assert_passes("email user gets mail")


def test_design_mail_notifier_knows_nothing_of_sms() -> None:
    assert "sms" not in _source(Path("Alerts/EmailNotifier.cs")).lower()


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    text = _source(Path("Alerts/AlertService.cs"))
    names = r"\bChannel\s*\.\s*(?:Sms|Email)\b|\"(?:sms|email)\""
    assert not re.search(names, text, flags=re.IGNORECASE), "the service names a channel"


def test_design_notifiers_share_an_abstract_type() -> None:
    assert _abstract_types("Alerts"), "no abstract type the notifiers share"
