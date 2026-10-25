"""Hidden checks for coupon-expiry: expiry is enforced, and the moment it compares against comes from outside."""

import re
import subprocess
from pathlib import Path

import pytest

HIDDEN = Path(__file__).parent


def _code(path: Path) -> str:
    """The Java source in `path` without its comments."""
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


@pytest.fixture(scope="module")
def build(tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("build")
    sources = sorted(str(path) for path in Path("src").rglob("*.java"))
    compiled = subprocess.run(
        ["javac", "-d", str(directory), *sources, str(HIDDEN / "HiddenChecks.java")],
        capture_output=True, text=True, check=False,
    )
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    return directory


def _check(build: Path, name: str) -> None:
    ran = subprocess.run(
        ["java", "-cp", str(build), "HiddenChecks", name], capture_output=True, text=True, timeout=60, check=False
    )
    assert ran.returncode == 0, ran.stdout + ran.stderr


# the system clock read directly; `Instant.now(clock)` and `clock.instant()` take it from outside
_CLOCK_READS = re.compile(
    r"\b(?:Instant|LocalDateTime|LocalDate|LocalTime|ZonedDateTime|OffsetDateTime)\s*\.\s*now\s*\(\s*\)"
    r"|\bSystem\s*\.\s*(?:currentTimeMillis|nanoTime)\s*\("
    r"|\bClock\s*\.\s*system\w*\s*\("
)
# the files that decide whether a coupon still holds
_DECISIONS = ("src/shop/CouponBook.java", "src/shop/Coupon.java")


def test_gate_valid_coupon_lowers_the_total(build: Path) -> None:
    _check(build, "valid")


def test_gate_expired_coupon_is_refused(build: Path) -> None:
    _check(build, "expired")


def test_design_coupons_never_read_the_clock_themselves() -> None:
    found = sorted(
        f"{name}: {match.group()}"
        for name in _DECISIONS
        if Path(name).exists()
        for match in _CLOCK_READS.finditer(_code(Path(name)))
    )
    assert not found, f"the coupons read the clock themselves: {found}"
