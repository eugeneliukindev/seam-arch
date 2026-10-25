"""Hidden checks for combo-checkout: coupon, VAT and charge are right; time comes from outside; VAT is data; Stripe gets no wrapper."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent
_NAMED = ("vat", "tax", "payment", "provider", "gateway", "processor")
_CLOCK = ("clock", "time")


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


def _sources() -> dict[str, str]:
    """Business code: every Go source but the tests and app.go, where the program is put together."""
    return {
        str(path): _code(path) for path in Path().rglob("*.go")
        if not path.name.endswith("_test.go") and path.name != "app.go" and "_hidden" not in str(path)
    }


def test_gate_coupon_vat_and_charge() -> None:
    _go_test("TestHiddenCouponVATAndCharge")


def test_gate_expired_coupon_is_refused() -> None:
    _go_test("TestHiddenExpiredCouponIsRefused")


def test_design_time_comes_from_outside() -> None:
    found = sorted(
        f"{name}: {call}" for name, code in _sources().items() for call in re.findall(r"\btime\.(?:Now|Since|Until)\b", code)
    )
    assert not found, f"business code reads the clock itself: {found}"


def _types(code: str) -> list[tuple[str, str]]:
    """Each declared type's name and the first word of its definition, alone or inside a `type (...)` group."""
    single = re.findall(r"\btype\s+(\w+)(?:\[[^\]]*\])?\s*=?\s*(\w+)", code)
    grouped = [
        pair for group in re.findall(r"\btype\s*\((.*?)\n\)", code, flags=re.DOTALL)
        for pair in re.findall(r"^\s*(\w+)(?:\[[^\]]*\])?\s*=?\s*(\w+)", group, flags=re.MULTILINE)
    ]
    return single + grouped


def test_design_no_type_for_vat_or_payment() -> None:
    extra = []
    for name, code in _sources().items():
        for type_name, kind in _types(code):
            lowered = type_name.lower()
            abstract = kind == "interface" and not any(word in lowered for word in _CLOCK)
            if abstract or any(word in lowered for word in _NAMED):
                extra.append(f"{name}: {type_name}")
    assert not extra, f"types for what is data or a single client: {sorted(set(extra))}"
