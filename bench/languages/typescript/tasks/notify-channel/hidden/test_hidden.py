"""Hidden checks for notify-channel: SMS works, and no shared unit branches on the channel name."""

import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent

_FAKES = """
import assert from "node:assert/strict";
import { buildService } from "../src/app.ts";
import { SmsGateway, SmtpClient } from "../src/gateways.ts";

class FakeSmtp extends SmtpClient {
  readonly sent: string[] = [];
  override sendMail(to: string, subject: string, body: string): void { this.sent.push(to); }
}

class FakeSms extends SmsGateway {
  readonly sent: string[] = [];
  override send(phone: string, text: string): void { this.sent.push(phone); }
}

const smtp = new FakeSmtp();
const sms = new FakeSms();
const service = buildService(smtp, sms);
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


_SHAPE = re.compile(r"\binterface\s+(\w+)|\btype\s+(\w+)\s*(?:<[^=]*>)?\s*=\s*(?=\{)")
_METHOD = re.compile(r"\w+\??\s*(?:<[^>]*>)?\s*\(|:\s*\([^)]*\)\s*=>")


def _contracts(paths: list[Path]) -> list[str]:
    """Abstract classes, and interfaces or object types that declare an operation."""
    found = []
    for path in paths:
        text = _source(path)
        found += re.findall(r"\babstract\s+class\s+(\w+)", text)
        for match in _SHAPE.finditer(text):
            if _METHOD.search(_body_after(text, match.end())):
                found.append(match.group(1) or match.group(2))
    return found


def test_gate_sms_user_gets_a_text() -> None:
    _run_ts(
        "gate_sms",
        _FAKES
        + """
service.alert({ id: 1, email: "a@example.com", phone: "+100", channel: "sms" }, "disk full");
assert.deepEqual(sms.sent, ["+100"]);
assert.deepEqual(smtp.sent, []);
""",
    )


def test_gate_email_user_gets_mail() -> None:
    _run_ts(
        "gate_email",
        _FAKES
        + """
service.alert({ id: 2, email: "b@example.com", phone: "+200", channel: "email" }, "disk full");
assert.deepEqual(smtp.sent, ["b@example.com"]);
assert.deepEqual(sms.sent, []);
""",
    )


_NAME = r"""(?:["'`](?:sms|email)["'`]|\w+\.(?:sms|email)\b)"""
_COMPARISON = re.compile(rf"(?:===?|!==?)\s*{_NAME}|{_NAME}\s*(?:===?|!==?)|\bcase\s+{_NAME}", re.IGNORECASE)


def test_design_mail_notifier_knows_nothing_of_sms() -> None:
    assert "sms" not in Path("src/email.ts").read_text(encoding="utf-8").lower()


def test_design_service_does_not_branch_on_the_channel_name() -> None:
    assert not _COMPARISON.search(_source(Path("src/service.ts")))


def test_design_notifiers_share_an_abstract_type() -> None:
    assert _contracts(sorted(Path("src").glob("*.ts"))), "no abstract type the notifiers share"
