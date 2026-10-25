"""Hidden checks for combo-checkout: coupon, VAT and charge are right; time comes from outside; VAT is data; Stripe gets no wrapper."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent
# the entry point, where the real clock is chosen
ENTRY = Path("src/app.rs")


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


def _sources() -> dict[str, str]:
    """The crate's business files, the entry point left out."""
    return {str(path): _code(path) for path in Path("src").rglob("*.rs") if path != ENTRY}


def test_gate_coupon_vat_and_charge() -> None:
    _cargo_test("valid_coupon")


def test_gate_expired_coupon_is_refused() -> None:
    _cargo_test("expired_coupon")


def test_design_time_comes_from_outside() -> None:
    found = sorted(
        f"{name}: {call}" for name, code in _sources().items()
        for call in re.findall(r"\b(?:SystemTime|Instant)\s*::\s*now\b", code)
    )
    assert not found, f"business code reads the clock itself: {found}"


def test_design_no_type_for_vat_or_payment() -> None:
    extra = []
    for name, code in _sources().items():
        for kind, declared in re.findall(r"\b(trait|struct|enum|type)\s+(\w+)", code):
            lowered = declared.lower()
            named = any(word in lowered for word in ("vat", "tax", "payment", "provider", "gateway", "processor"))
            clock = any(word in lowered for word in ("clock", "time"))
            if (kind == "trait" and declared != "StripeClient" and not clock) or named:
                extra.append(f"{name}: {kind} {declared}")
    assert not extra, f"types for what is data or a single client: {extra}"
