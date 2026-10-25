"""Hidden checks for combo-checkout: coupon, VAT and charge are right; time comes from outside; VAT is data; Stripe gets no wrapper."""

import re
import subprocess
from functools import cache
from pathlib import Path

_CHECK = Path(__file__).parent / "Check"
# the entry point is where the real clock is chosen
_ENTRY_POINT = "App.cs"


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


def _business_sources() -> dict[Path, str]:
    return {
        path: _source(path)
        for path in Path("Shop").rglob("*.cs")
        if not {"bin", "obj"} & set(path.parts) and path.name != _ENTRY_POINT
    }


def test_gate_coupon_vat_and_charge() -> None:
    _assert_passes("valid coupon and GB VAT are charged")


def test_gate_expired_coupon_is_refused() -> None:
    _assert_passes("expired coupon is refused and nothing charged")


def test_design_time_comes_from_outside() -> None:
    clock = re.compile(r"\bDateTime(?:Offset)?\s*\.\s*(?:Now|UtcNow|Today)\b|\bTimeProvider\s*\.\s*System\b")
    found = sorted(f"{path}: {match}" for path, text in _business_sources().items() for match in clock.findall(text))
    assert not found, f"business code reads the clock itself: {found}"


def test_design_no_type_for_vat_or_payment() -> None:
    abstract = re.compile(r"\binterface\s+(\w+)|\babstract\s+(?:partial\s+)?(?:class|record)\s+(\w+)")
    extra = sorted(
        f"{path}: {first or second}"
        for path, text in _business_sources().items()
        for first, second in abstract.findall(text)
        if not re.search(r"clock|time", first or second, re.IGNORECASE)
    )
    assert not extra, f"abstract types for what is data or a single client: {extra}"
