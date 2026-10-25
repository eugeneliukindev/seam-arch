"""Hidden checks for combo-alerts: three channels deliver, and after two edits no shared unit branches on the channel."""

import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent

_FAKES = """
import assert from "node:assert/strict";
import { buildService } from "../src/app.ts";
import { PushGateway, SmsGateway, SmtpClient } from "../src/gateways.ts";

class FakeSmtp extends SmtpClient {
  readonly sent: string[] = [];
  override sendMail(to: string, subject: string, body: string): void { this.sent.push(to); }
}

class FakeSms extends SmsGateway {
  readonly sent: string[] = [];
  override send(phone: string, text: string): void { this.sent.push(phone); }
}

class FakePush extends PushGateway {
  readonly sent: string[] = [];
  override send(deviceToken: string, text: string): void { this.sent.push(deviceToken); }
}

function deliveries(user: any): number[] {
  const smtp = new FakeSmtp();
  const sms = new FakeSms();
  const push = new FakePush();
  buildService(smtp, sms, push).alert(user, "disk full");
  return [smtp.sent.length, sms.sent.length, push.sent.length];
}

const user = (channel: string) => ({ id: 1, email: "a@example.com", phone: "+100", deviceToken: "dev-1", channel });
"""


def _run_ts(name: str, source: str) -> None:
    script = HERE / f"{name}.ts"
    script.write_text(source, encoding="utf-8")
    completed = subprocess.run(["tsx", str(script)], capture_output=True, text=True, timeout=60, check=False)
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _source(path: Path) -> str:
    """The code of a TypeScript file, comments removed."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"(?m)^\s*//.*$|\s//.*$", "", text)


def _body_after(text: str, start: int) -> str:
    """The text inside the braces opening at or after `start`."""
    opening = text.find("{", start)
    depth = 0
    for index in range(opening, len(text)):
        depth += {"{": 1, "}": -1}.get(text[index], 0)
        if depth == 0:
            return text[opening + 1 : index]
    return text[opening + 1 :]


def _top_level(body: str) -> str:
    """`body` with the inside of every nested brace, bracket and parenthesis removed."""
    flat, depth = [], 0
    for char in body:
        if char in "{[(":
            depth += 1
            if depth == 1:
                flat.append(char)
        elif char in "}])":
            depth -= 1
            if depth == 0:
                flat.append(char)
        elif depth == 0:
            flat.append(char)
    return "".join(flat)


def test_gate_each_channel_delivers() -> None:
    _run_ts(
        "gate_channels",
        _FAKES
        + """
assert.deepEqual(deliveries(user("email")), [1, 0, 0], "email");
assert.deepEqual(deliveries(user("sms")), [0, 1, 0], "sms");
assert.deepEqual(deliveries(user("push")), [0, 0, 1], "push");
""",
    )


_NAME = r"""(?:["'`](?:sms|email|push)["'`]|\w+\.(?:sms|email|push)\b)"""
_COMPARISON = re.compile(rf"(?:===?|!==?)\s*{_NAME}|{_NAME}\s*(?:===?|!==?)|\bcase\s+{_NAME}", re.IGNORECASE)
# `push` as a word, not the array method
_PUSH = re.compile(r"(?<!\.)\bpush\b(?!\s*\()", re.IGNORECASE)


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    assert not _COMPARISON.search(_source(Path("src/service.ts")))


def test_design_each_notifier_knows_only_its_channel() -> None:
    email = _source(Path("src/email.ts"))
    assert "sms" not in email.lower(), "src/email.ts knows of text messages"
    assert not _PUSH.search(email), "src/email.ts knows of push"
    sms = Path("src/sms.ts")
    assert not sms.exists() or not _PUSH.search(_source(sms)), "src/sms.ts knows of push"


def test_gate_sms_without_phone_falls_back_to_mail() -> None:
    _run_ts(
        "gate_fallback",
        _FAKES
        + """
assert.deepEqual(deliveries({ id: 3, email: "c@example.com", channel: "sms" }), [1, 0, 0]);
""",
    )


_CONTRACT = re.compile(r"\babstract\s+class\s+(\w+)|\binterface\s+(\w+)|\btype\s+(\w+)\s*(?:<[^=]*>)?\s*=\s*(?=\{)")
# a member that is an operation: a method signature, or a property whose type is a function
_OPERATION = re.compile(
    r"(?m)^\s*(?:(?:public|protected|private|abstract|readonly|static|async)\s+)*(?!constructor\b)(\w+)\??\s*(?:<[^>]*>)?\s*(?:\(\)|:\s*\(\)\s*=>)"
)


def test_design_notifier_contract_is_narrow() -> None:
    wide = {}
    for path in sorted(Path("src").glob("*.ts")):
        text = _source(path)
        for match in _CONTRACT.finditer(text):
            operations = _OPERATION.findall(_top_level(_body_after(text, match.end())))
            if len(operations) > 1:
                wide[f"{path}: {match.group(1) or match.group(2) or match.group(3)}"] = operations
    assert not wide, f"a contract that asks for more than delivering one alert: {wide}"


_NOTIFIER = re.compile(r"(?<!abstract )\bclass\s+(\w*Notifier)\b")
_REFUSAL = re.compile(r"\bthrow\b[^;]*(?:not\s*implemented|unsupported|not\s+supported)", re.IGNORECASE)


def test_design_every_notifier_honours_the_contract() -> None:
    refusing = [
        f"{path}: {match.group(1)}"
        for path in sorted(Path("src").glob("*.ts"))
        for text in [_source(path)]
        for match in _NOTIFIER.finditer(text)
        if _REFUSAL.search(_body_after(text, match.end()))
    ]
    assert not refusing, f"notifiers that refuse part of the contract: {refusing}"
