"""Hidden checks for coupon-expiry: expiry is enforced, and the moment it compares against comes from outside."""

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


_SETUP = """
import assert from "node:assert/strict";
import { buildBook } from "../src/app.ts";

const book: any = buildBook();
"""


def test_gate_valid_coupon_lowers_the_total() -> None:
    _run_ts(
        "gate_valid",
        _SETUP
        + """
book.add({ code: "A", percent: 10, expires: new Date("2100-01-01T00:00:00Z") });
const total = await book.apply("A", 100);
assert.ok(Math.abs(total - 90) < 1e-9, `got ${total}`);
""",
    )


def test_gate_expired_coupon_is_refused() -> None:
    _run_ts(
        "gate_expired",
        _SETUP
        + """
book.add({ code: "A", percent: 10, expires: new Date("2000-01-01T00:00:00Z") });
let refused: any;
try {
  await book.apply("A", 100);
} catch (error) {
  refused = error;
}
assert.ok(refused, "an expired coupon was accepted");
assert.ok([refused?.name, refused?.constructor?.name].includes("CouponExpiredError"), `${refused}`);
""",
    )


# `new Date` with nothing, or with empty parentheses, is the current moment
_CLOCK = re.compile(r"\bDate\.now\s*\(|\bnew\s+Date\b(?!\s*\(\s*[^\s)])|\bperformance\.now\s*\(|\bTemporal\.Now\b")


def test_design_coupons_never_read_the_clock_themselves() -> None:
    found = [match.group() for match in _CLOCK.finditer(_source(Path("src/coupons.ts")))]
    assert not found, f"src/coupons.ts reads the clock itself: {found}"
