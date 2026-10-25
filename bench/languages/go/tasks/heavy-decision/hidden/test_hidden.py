"""Hidden checks for heavy-decision: the file read is passed in, the grading rules are used directly."""

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


def test_gate_summary_of_a_file() -> None:
    _go_test("TestHiddenSummaryOfAFile")


def test_design_reading_is_passed_in() -> None:
    code = _code(Path("service.go"))
    found = re.findall(r"\bReadTextFile\b|\bos\.\w+|\bioutil\.\w+|\"os\"|\"io/ioutil\"", code)
    assert not found, f"service.go reads the file itself: {sorted(set(found))}"


def test_design_grading_is_used_directly() -> None:
    assert re.search(r"\bGradeOf\(", _code(Path("service.go"))), "the grading rules are the decision"
