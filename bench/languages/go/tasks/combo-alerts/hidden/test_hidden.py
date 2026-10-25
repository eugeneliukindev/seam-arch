"""Hidden checks for combo-alerts: three channels deliver with a mail fallback, and the notifiers keep to one narrow contract."""

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


def test_gate_sms_without_phone_falls_back_to_mail() -> None:
    _go_test("TestHiddenSmsWithoutPhoneFallsBackToMail")


def _interfaces() -> dict[str, list[str]]:
    """Each declared interface's name and the methods it asks for, embedded interfaces aside."""
    found = {}
    for path in _sources():
        code = _code(path)
        for match in re.finditer(r"\b(\w+)\s+interface\s*\{", code):
            depth, end = 1, match.end()
            while depth and end < len(code):
                depth += {"{": 1, "}": -1}.get(code[end], 0)
                end += 1
            body = code[match.end():end - 1]
            found[match.group(1)] = re.findall(r"(?:^|[;{\n])\s*(\w+)\s*\(", body)
    return found


def test_design_notifier_contract_is_narrow() -> None:
    wide = {name: methods for name, methods in _interfaces().items() if len(methods) > 1}
    assert not wide, f"a contract that asks for more than delivering one alert: {wide}"


def test_design_every_notifier_honours_the_contract() -> None:
    refusal = re.compile(r"\bpanic\s*\(|not\s+(?:yet\s+)?(?:implemented|supported)|unsupported", re.IGNORECASE)
    refusing = sorted(
        f"{path}: {receiver}.{method}"
        for path in _sources()
        for receiver, method, body in re.findall(
            r"^func\s*\(\s*\w*\s*\*?\s*(\w*Notifier)\s*\)\s*(\w+)\s*\(.*?\{(.*?)^\}", _code(path), flags=re.DOTALL | re.MULTILINE
        )
        if refusal.search(body)
    )
    assert not refusing, f"notifiers that refuse part of the contract: {refusing}"
