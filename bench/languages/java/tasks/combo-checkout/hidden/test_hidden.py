"""Hidden checks for combo-checkout: coupon, VAT and charge are right; time comes from outside; VAT is data; Stripe gets no wrapper."""

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


def _sources() -> dict[str, str]:
    """The business code: every source but the entry point."""
    return {str(path): _code(path) for path in Path("src").rglob("*.java") if path.name != "App.java"}


# the system clock read directly; `Instant.now(clock)` and `clock.instant()` take it from outside
_CLOCK_READS = re.compile(
    r"\b(?:Instant|LocalDateTime|LocalDate|LocalTime|ZonedDateTime|OffsetDateTime)\s*\.\s*now\s*\(\s*\)"
    r"|\bSystem\s*\.\s*(?:currentTimeMillis|nanoTime)\s*\("
    r"|\bClock\s*\.\s*system\w*\s*\("
)
_ABSTRACT = re.compile(r"\b(?:interface|abstract\s+(?:(?:sealed|non-sealed)\s+)?class)\s+(\w+)")
_CLASS = re.compile(r"\bclass\s+(\w+)")
_DATA_OR_ONE_CLIENT = ("vat", "tax", "payment", "provider", "gateway", "processor")


def test_gate_coupon_vat_and_charge(build: Path) -> None:
    _check(build, "valid")


def test_gate_expired_coupon_is_refused(build: Path) -> None:
    _check(build, "expired")


def test_design_time_comes_from_outside() -> None:
    found = sorted(f"{name}: {match.group()}" for name, code in _sources().items() for match in _CLOCK_READS.finditer(code))
    assert not found, f"business code reads the clock itself: {found}"


def test_design_no_type_for_vat_or_payment() -> None:
    extra = sorted(
        f"{name}: {type_name}"
        for name, code in _sources().items()
        for type_name in {*_ABSTRACT.findall(code), *_CLASS.findall(code)}
        if (type_name in _ABSTRACT.findall(code) and not any(word in type_name.lower() for word in ("clock", "time")))
        or any(word in type_name.lower() for word in _DATA_OR_ONE_CLIENT)
    )
    assert not extra, f"types for what is data or a single client: {extra}"
