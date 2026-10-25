"""Hidden checks for speculative-abstraction: Stripe works, and no abstract type is added for one implementation."""

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


def test_gate_charges_in_cents() -> None:
    _run_ts(
        "gate_cents",
        """
import assert from "node:assert/strict";
import { charge } from "../src/payments.ts";
import { StripeClient } from "../src/stripe-client.ts";

class FakeStripe extends StripeClient {
  readonly charges: Array<[number, string, string]> = [];
  override async createCharge({ amountCents, currency, source }: { amountCents: number; currency: string; source: string }): Promise<string> {
    // Stripe itself takes the code in lower case; the case is not the point of the task
    this.charges.push([amountCents, currency.toUpperCase(), source]);
    return "ch_1";
  }
}

const stripe = new FakeStripe();
assert.equal(await charge({ id: 1, total: 19.5, currency: "EUR" }, { cardToken: "tok_1", client: stripe }), "ch_1");
assert.deepEqual(stripe.charges, [[1950, "EUR", "tok_1"]]);
""",
    )


def test_design_no_abstract_type_for_one_implementation() -> None:
    found = _contracts(sorted(Path("src").glob("*.ts")))
    assert not found, f"abstract types under a single implementation: {found}"
