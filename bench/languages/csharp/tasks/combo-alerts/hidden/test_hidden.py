"""Hidden checks for combo-alerts: three channels deliver, and after two edits no shared unit branches on the channel."""

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


def test_gate_sms_without_phone_falls_back_to_mail() -> None:
    _assert_passes("sms user without a phone gets mail")


def _members(body: str) -> list[str]:
    """The members declared directly in a type's body: nested blocks fold away, each declaration ends in `;`."""
    flat, depth = [], 0
    for character in body:
        if character == "{":
            depth += 1
            if depth == 1:
                continue
        elif character == "}":
            depth -= 1
            if depth == 1:
                flat.append(";")
            continue
        if depth == 1:
            flat.append(character)
    return [member.strip() for member in "".join(flat).split(";") if member.strip()]


def _contracts() -> dict[str, list[str]]:
    """Each interface and abstract class under Alerts, with the members an implementation must supply."""
    found = {}
    for text in _sources("Alerts").values():
        for match in re.finditer(r"\binterface\s+(\w+)|\babstract\s+(?:partial\s+)?(?:class|record)\s+(\w+)", text):
            opening = text.find("{", match.end())
            depth = 0
            for index in range(opening, len(text)):
                depth += {"{": 1, "}": -1}.get(text[index], 0)
                if depth == 0:
                    break
            members = _members(text[opening:index + 1])
            if match.group(2):
                members = [member for member in members if re.search(r"\b(?:abstract|virtual)\b", member)]
            found[match.group(1) or match.group(2)] = members
    return found


def test_design_notifier_contract_is_narrow() -> None:
    wide = {name: members for name, members in _contracts().items() if len(members) > 1}
    assert not wide, f"a contract that asks for more than delivering one alert: {wide}"


def test_design_every_notifier_honours_the_contract() -> None:
    contracts = _contracts()
    refusing = sorted(
        name
        for name, text in _types("Alerts").items()
        if name.endswith("Notifier")
        and name not in contracts
        and re.search(r"\bNot(?:Implemented|Supported)Exception\b", text)
    )
    assert not refusing, f"notifiers that refuse part of the contract: {refusing}"
