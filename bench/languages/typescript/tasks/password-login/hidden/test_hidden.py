"""Hidden checks for password-login: passwords work, and hashing sits behind a contract."""

import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent


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


def test_gate_right_password_logs_in() -> None:
    _run_ts(
        "gate_right",
        """
import assert from "node:assert/strict";
import { buildService } from "../src/app.ts";

const service = buildService();
await service.register("a@example.com", "s3cret");
assert.equal(await service.logIn("a@example.com", "s3cret"), true);
""",
    )


def test_gate_wrong_password_or_email_fails() -> None:
    _run_ts(
        "gate_wrong",
        """
import assert from "node:assert/strict";
import { buildService } from "../src/app.ts";

const service = buildService();
await service.register("a@example.com", "s3cret");
assert.equal(await service.logIn("a@example.com", "guess"), false);
assert.equal(await service.logIn("b@example.com", "s3cret"), false);
""",
    )


def test_design_service_does_not_hash_itself() -> None:
    found = re.findall(r"""["'](?:node:)?crypto["']""", _source(Path("src/service.ts")))
    assert not found, "src/service.ts uses the mechanism directly: node:crypto"


def test_design_hashing_has_an_abstract_contract() -> None:
    contracts = set(_contracts(sorted(Path("src").glob("*.ts")))) - {"UserStore"}
    assert contracts, "no abstract contract besides UserStore"
