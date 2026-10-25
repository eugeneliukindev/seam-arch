"""Hidden checks for plain-records: the advice is right, and it decides on a record, not the provider's JSON."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent
PROVIDER_KEYS = {"daily", "pop", "tmax"}


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


def test_gate_umbrella_advice() -> None:
    _cargo_test("umbrella")


def test_design_advice_never_reads_the_provider_format() -> None:
    literals = set(re.findall(r"\"((?:[^\"\\]|\\.)*)\"", _code(Path("src/advice.rs"))))
    keys = sorted(literals & PROVIDER_KEYS)
    assert not keys, f"advice digs into the provider's JSON: {keys}"
