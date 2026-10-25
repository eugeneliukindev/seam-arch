"""Hidden checks for speculative-abstraction: Stripe works, and no interface is added for one implementation."""

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


def test_gate_charges_in_cents() -> None:
    _go_test("TestHiddenChargesInCents")


def test_design_no_interface_for_one_implementation() -> None:
    sources = [path for path in Path().rglob("*.go") if not path.name.endswith("_test.go") and "_hidden" not in str(path)]
    found = {name for path in sources for name in re.findall(r"\btype\s+(\w+)\s+interface\b", _code(path))}
    assert not found, f"interfaces over a single implementation: {sorted(found)}"
