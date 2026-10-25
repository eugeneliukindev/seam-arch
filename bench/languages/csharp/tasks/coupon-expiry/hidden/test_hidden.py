"""Hidden checks for coupon-expiry: expiry is enforced, and the moment it compares against comes from outside."""

import re
import subprocess
from functools import cache
from pathlib import Path

_CHECK = Path(__file__).parent / "Check"


@cache
def _check_output() -> str:
    """What the check program prints: one `PASS <scenario>` or `FAIL <scenario>: <why>` per line."""
    completed = subprocess.run(
        ["dotnet", "run", "--project", str(_CHECK)], capture_output=True, text=True, check=False
    )
    return completed.stdout + completed.stderr


def _assert_passes(scenario: str) -> None:
    assert f"PASS {scenario}" in _check_output().splitlines(), _check_output()


def _source(path: Path) -> str:
    """C# source without its comments."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


def test_gate_valid_coupon_lowers_the_total() -> None:
    _assert_passes("valid coupon lowers the total")


def test_gate_expired_coupon_is_refused() -> None:
    _assert_passes("expired coupon is refused")


def test_design_coupons_never_read_the_clock_themselves() -> None:
    clock = re.compile(r"\bDateTime(?:Offset)?\s*\.\s*(?:Now|UtcNow|Today)\b|\bTimeProvider\s*\.\s*System\b")
    found = sorted(set(clock.findall(_source(Path("Shop/Coupons.cs")))))
    assert not found, f"Shop/Coupons.cs reads the clock itself: {found}"
