"""Hidden checks for second-channel: three channels deliver, and after two edits no shared unit branches on the channel."""

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
