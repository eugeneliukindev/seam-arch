"""Hidden checks for combo-alerts: three channels deliver, a phoneless texter gets mail, and the notifier contract holds."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent
# the clients the seed gives; contracts the agent writes are the others
GATEWAYS = {"SmtpClient", "SmsGateway", "PushGateway"}


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


def test_gate_sms_without_phone_falls_back_to_mail() -> None:
    _cargo_test("sms_fallback")


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    found = re.findall(r"\b(?:Sms|Email|Push|SMS|EMAIL|PUSH)\b|\"(?i:sms|email|push)\"", _code(Path("src/service.rs")))
    assert not found, f"src/service.rs names channels: {sorted(set(found))}"


def test_design_each_notifier_knows_only_its_channel() -> None:
    email = _code(Path("src/email.rs")).lower()
    assert "sms" not in email and "push" not in email, "src/email.rs knows of other channels"
    assert "push" not in _code(Path("src/sms.rs")).lower(), "src/sms.rs knows of push"


def _block(code: str, start: int) -> str:
    """The text inside the braces that open at or after `start`."""
    opening = code.index("{", start)
    depth = 0
    for position in range(opening, len(code)):
        depth += {"{": 1, "}": -1}.get(code[position], 0)
        if depth == 0:
            return code[opening + 1 : position]
    return code[opening + 1 :]


def _outermost(body: str) -> str:
    """`body` with every nested block taken out: what a trait or impl declares itself."""
    kept, depth = [], 0
    for character in body:
        depth -= character == "}"
        if depth == 0:
            kept.append(character)
        depth += character == "{"
    return "".join(kept)


def _sources() -> dict[str, str]:
    return {str(path): _code(path) for path in Path("src").rglob("*.rs")}


def _contracts() -> dict[str, list[str]]:
    """Each trait the crate declares beyond the gateways, with the methods it asks for."""
    found = {}
    for code in _sources().values():
        for match in re.finditer(r"\btrait\s+(\w+)[^{;]*\{", code):
            if match.group(1) not in GATEWAYS:
                found[match.group(1)] = re.findall(r"\bfn\s+(\w+)", _outermost(_block(code, match.start())))
    return found


def test_design_notifier_contract_is_narrow() -> None:
    wide = {name: methods for name, methods in _contracts().items() if len(methods) > 1}
    assert not wide, f"a contract that asks for more than delivering one alert: {wide}"


def test_design_every_notifier_honours_the_contract() -> None:
    contracts = set(_contracts())
    refused = [
        f"{name}: impl {match.group(1)} for {match.group(2).strip()}"
        for name, code in _sources().items()
        for match in re.finditer(r"\bimpl\b(?:\s*<[^{]*?>)?\s+(\w+)(?:<[^{]*?>)?\s+for\s+([^{]+)\{", code)
        if match.group(1) in contracts and re.search(r"\b(?:unimplemented|todo)\s*!", _block(code, match.start()))
    ]
    assert not refused, f"an implementation refuses part of the contract: {refused}"
