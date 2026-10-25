"""Hidden checks for second-channel: three channels deliver, and after two edits no shared unit branches on the channel."""

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


def _types(directory: str) -> dict[str, str]:
    """Each class, record or struct under `directory`: its name and its text, header and body."""
    found = {}
    for text in _sources(directory).values():
        for match in re.finditer(r"\b(?:class|record|struct)\s+(\w+)", text):
            parens = braces = 0
            for index in range(match.end(), len(text)):
                character = text[index]
                parens += {"(": 1, ")": -1}.get(character, 0)
                braces += {"{": 1, "}": -1}.get(character, 0) if parens == 0 else 0
                if parens == braces == 0 and character in ";}":
                    break
            found[match.group(1)] = text[match.start():index + 1]
    return found


def test_gate_each_channel_delivers() -> None:
    for scenario in ("email user gets mail", "sms user gets a text", "push user gets a notification"):
        _assert_passes(scenario)


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    text = _source(Path("Alerts/AlertService.cs"))
    names = r"\bChannel\s*\.\s*(?:Sms|Email|Push)\b|\"(?:sms|email|push)\""
    assert not re.search(names, text, flags=re.IGNORECASE), "the service names a channel"


def test_design_each_notifier_knows_only_its_channel() -> None:
    mail = _source(Path("Alerts/EmailNotifier.cs")).lower()
    assert "sms" not in mail and "push" not in mail, "the mail notifier knows the other channels"
    texts = {name: text for name, text in _types("Alerts").items() if "sms" in name.lower()}
    knowing = sorted(name for name, text in texts.items() if "push" in text.lower())
    assert not knowing, f"the text notifier knows push: {knowing}"
