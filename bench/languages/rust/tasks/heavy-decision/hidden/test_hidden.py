"""Hidden checks for heavy-decision: the file read is passed in, the grading rules are used directly."""

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



def test_gate_summary_of_a_file() -> None:
    _cargo_test("summary")


def test_design_reading_is_passed_in() -> None:
    found = re.findall(r"\b(?:fs|File|files|read_text_file)\b", _code(Path("src/service.rs")))
    assert not found, f"src/service.rs reads the file itself: {sorted(set(found))}"


def test_design_grading_is_used_directly() -> None:
    assert re.search(r"\bgrade_of\b", _code(Path("src/service.rs"))), "the grading rules are the decision"
