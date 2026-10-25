"""Hidden checks for heavy-decision: the file read is passed in, the grading rules are used directly."""

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


def test_gate_summary_of_a_file(build: Path) -> None:
    _check(build, "summary")


def test_design_reading_is_passed_in() -> None:
    code = _code(Path("src/resumes/ResumeService.java"))
    # the reader may be a field or parameter of any name; what must not appear is the file module itself
    assert not re.search(r"\b(?:ResumeFiles|Files\s*(?:\.|::)\s*read\w*)\b", code), "the service reads the file itself"


def test_design_grading_is_used_directly() -> None:
    code = _code(Path("src/resumes/ResumeService.java"))
    assert re.search(r"\bgradeOf\s*\(", code), "the grading rules are the decision"
