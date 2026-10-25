"""Hidden checks for coupon-expiry: expiry is enforced, and the moment it compares against comes from outside."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent


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
    """The Rust source of `path` without comments."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


def test_gate_valid_coupon_lowers_the_total() -> None:
    _cargo_test("valid_coupon")


def test_gate_expired_coupon_is_refused() -> None:
    _cargo_test("expired_coupon")


def test_design_coupons_never_read_the_clock_themselves() -> None:
    found = sorted(set(re.findall(r"\b(?:SystemTime|Instant)\s*::\s*now\b", _code(Path("src/coupons.rs")))))
    assert not found, f"src/coupons.rs reads the clock itself: {found}"
