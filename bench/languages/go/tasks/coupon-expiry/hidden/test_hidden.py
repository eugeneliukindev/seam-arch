"""Hidden checks for coupon-expiry: expiry is enforced, and the moment it compares against comes from outside."""

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


def test_gate_valid_coupon_lowers_the_total() -> None:
    _go_test("TestHiddenValidCouponLowersTheTotal")


def test_gate_expired_coupon_is_refused() -> None:
    _go_test("TestHiddenExpiredCouponIsRefused")


def test_design_coupons_never_read_the_clock_themselves() -> None:
    found = sorted(set(re.findall(r"\btime\.(?:Now|Since|Until)\b", _code(Path("coupons.go")))))
    assert not found, f"coupons.go reads the clock itself: {found}"
