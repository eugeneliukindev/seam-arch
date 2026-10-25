"""Hidden checks for speculative-abstraction: Stripe works, and no trait is added for one implementation."""

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
    """The Rust source of `path` without comments; empty when the file does not exist."""
    if not path.exists():
        return ""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


def _traits() -> set[str]:
    """Names of the traits the crate declares."""
    return {name for path in Path("src").rglob("*.rs") for name in re.findall(r"\btrait\s+(\w+)", _code(path))}



def test_gate_charges_in_cents() -> None:
    _cargo_test("charge")


def test_design_no_trait_for_one_implementation() -> None:
    added = _traits() - {"StripeClient"}
    assert not added, f"traits under a single implementation: {sorted(added)}"
