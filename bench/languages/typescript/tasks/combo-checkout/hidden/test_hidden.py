"""Hidden checks for combo-checkout: coupon, VAT and charge are right; time comes from outside; VAT is data; Stripe gets no wrapper."""

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


# the checkout under test, with a coupon TEN that expires at `expires`, charging through a fake Stripe
_SETUP = """
import assert from "node:assert/strict";
import { buildCheckout } from "../src/app.ts";
import { StripeClient } from "../src/stripe-client.ts";

class FakeStripe extends StripeClient {
  readonly charges: number[] = [];
  override async createCharge({ amountCents }: { amountCents: number; currency: string; source: string }): Promise<string> {
    this.charges.push(amountCents);
    return "ch_1";
  }
}

const stripe = new FakeStripe();
const checkout: any = buildCheckout(stripe);
const book: any = Object.values(checkout).find((value: any) => typeof value?.add === "function");
assert.ok(book, "the checkout holds no coupon book");
"""


def test_gate_coupon_vat_and_charge() -> None:
    _run_ts(
        "gate_charge",
        _SETUP
        + """
book.add({ code: "TEN", percent: 10, expires: new Date("2100-01-01T00:00:00Z") });
assert.equal(await checkout.pay({ total: 100 }, "TEN", "GB", "tok"), "ch_1");
assert.deepEqual(stripe.charges, [10800]);
""",
    )


def test_gate_expired_coupon_is_refused() -> None:
    _run_ts(
        "gate_expired",
        _SETUP
        + """
book.add({ code: "TEN", percent: 10, expires: new Date("2000-01-01T00:00:00Z") });
let refused: any;
try {
  await checkout.pay({ total: 100 }, "TEN", "DE", "tok");
} catch (error) {
  refused = error;
}
assert.ok(refused, "an expired coupon was accepted");
assert.match(`${refused?.name} ${refused?.constructor?.name} ${refused?.message}`, /TEN|expir/i);
assert.deepEqual(stripe.charges, []);
""",
    )


# `new Date` with nothing, or with empty parentheses, is the current moment
_CLOCK = re.compile(r"\bDate\.now\s*\(|\bnew\s+Date\b(?!\s*\(\s*[^\s)])|\bperformance\.now\s*\(|\bTemporal\.Now\b")


def _business_files() -> list[Path]:
    return sorted(path for path in Path("src").rglob("*.ts") if path.name != "app.ts")


def test_design_time_comes_from_outside() -> None:
    found = [f"{path}: {match.group()}" for path in _business_files() for match in _CLOCK.finditer(_source(path))]
    assert not found, f"business code reads the clock itself: {found}"


_SHAPE = re.compile(r"\binterface\s+(\w+)|\btype\s+(\w+)\s*(?:<[^=]*>)?\s*=\s*(?=\{)")
_METHOD = re.compile(r"\w+\??\s*(?:<[^>]*>)?\s*\(|:\s*\([^)]*\)\s*=>")
_NAMED = re.compile(r"\b(?:interface|type|class)\s+(\w+)")
_FOR_DATA_OR_ONE_CLIENT = ("vat", "tax", "payment", "provider", "gateway", "processor")
_FOR_TIME = ("clock", "time")


def test_design_no_type_for_vat_or_payment() -> None:
    extra = []
    for path in _business_files():
        text = _source(path)
        contracts = re.findall(r"\babstract\s+class\s+(\w+)", text)
        contracts += [
            match.group(1) or match.group(2)
            for match in _SHAPE.finditer(text)
            if _METHOD.search(_body_after(text, match.end()))
        ]
        named = [name for name in _NAMED.findall(text) if any(word in name.lower() for word in _FOR_DATA_OR_ONE_CLIENT)]
        extra += [
            f"{path}: {name}"
            for name in sorted({*contracts, *named})
            if name in named or not any(word in name.lower() for word in _FOR_TIME)
        ]
    assert not extra, f"types for what is data or a single client: {extra}"
