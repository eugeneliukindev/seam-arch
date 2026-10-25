"""Hidden checks for combo-alerts: three channels deliver, a missing phone falls back to mail, and the notifiers share one narrow contract every one of them honours."""

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


_NAME = r"(?:\w+\s*\.\s*)?(?:SMS|EMAIL|PUSH|\"sms\"|\"email\"|\"push\")"
_BRANCHES = (
    rf"(?:==|!=)\s*{_NAME}\b",
    rf"\b{_NAME}\s*(?:==|!=)",
    rf"\.\s*equals(?:IgnoreCase)?\s*\(\s*{_NAME}",
    rf"{_NAME}\s*\.\s*equals",
    rf"\bcase\s+{_NAME}",
    r"\bswitch\s*\([^)]*channel",
)


def test_gate_each_channel_delivers(build: Path) -> None:
    _check(build, "each")


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    code = _code(Path("src/alerts/AlertService.java"))
    found = [pattern for pattern in _BRANCHES if re.search(pattern, code, flags=re.IGNORECASE)]
    assert not found, f"the service branches on the channel: {found}"


def test_design_each_notifier_knows_only_its_channel() -> None:
    mail = Path("src/alerts/EmailNotifier.java").read_text(encoding="utf-8").lower()
    assert "sms" not in mail
    assert "push" not in mail
    sms = Path("src/alerts/SmsNotifier.java")
    assert not sms.exists() or "push" not in sms.read_text(encoding="utf-8").lower()


def test_gate_sms_without_phone_falls_back_to_mail(build: Path) -> None:
    _check(build, "fallback")


def _block(code: str, start: int) -> str:
    """The block whose brace opens at or after `start`, braces included."""
    opening, depth = code.index("{", start), 0
    for index in range(opening, len(code)):
        depth += {"{": 1, "}": -1}.get(code[index], 0)
        if depth == 0:
            return code[opening : index + 1]
    return code[opening:]


def _top_level(block: str) -> str:
    """The inside of `block` with every nested block emptied to `{}`."""
    depth, kept = 0, []
    for char in block[1:-1]:
        if char == "{":
            depth += 1
            kept.append("{}" if depth == 1 else "")
        elif char == "}":
            depth -= 1
        elif depth == 0:
            kept.append(char)
    return "".join(kept)


_CONTRACT = re.compile(r"\b(?:interface|abstract\s+(?:(?:sealed|non-sealed)\s+)?class)\s+(\w+)")
_MEMBER = re.compile(r"(?:[^=]*\s)?(\w+)\s*\([^()]*\)\s*(?:throws\s[^;{]*)?")


def _contract_methods(name: str, block: str) -> list[str]:
    """The methods a contract asks its implementations for: neither static nor private, constructors aside."""
    methods = []
    for member in re.split(r";|\{\}", _top_level(block)):
        head = member.strip()
        match = _MEMBER.fullmatch(head)
        if match and match.group(1) != name and not re.search(r"\b(?:static|private)\b", head):
            methods.append(match.group(1))
    return methods


def _contracts() -> dict[str, list[str]]:
    found = {}
    for path in Path("src/alerts").glob("*.java"):
        code = _code(path)
        for match in _CONTRACT.finditer(code):
            found[match.group(1)] = _contract_methods(match.group(1), _block(code, match.end()))
    return found


def test_design_notifier_contract_is_narrow() -> None:
    wide = {name: methods for name, methods in _contracts().items() if len(methods) > 1}
    assert not wide, f"a contract that asks for more than delivering one alert: {wide}"


_NOTIFIER = re.compile(r"\b(?:class|record|enum)\s+(\w*Notifier)\b")


def test_design_every_notifier_honours_the_contract() -> None:
    refusing = []
    for path in Path("src/alerts").glob("*.java"):
        code = _code(path)
        for match in _NOTIFIER.finditer(code):
            modifiers = re.split(r"[;{}]", code[: match.start()])[-1]
            if not re.search(r"\babstract\b", modifiers) and "UnsupportedOperationException" in _block(code, match.end()):
                refusing.append(match.group(1))
    assert not refusing, f"notifiers that refuse part of the contract: {refusing}"
