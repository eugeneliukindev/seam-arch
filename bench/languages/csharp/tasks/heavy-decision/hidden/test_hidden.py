"""Hidden checks for heavy-decision: the file read is passed in, the grading rules are used directly."""

import re
import subprocess
from functools import cache
from pathlib import Path

_CHECK = Path(__file__).parent / "Check"


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


def _sources(directory: str) -> dict[Path, str]:
    return {
        path: _source(path)
        for path in Path(directory).rglob("*.cs")
        if not {"bin", "obj"} & set(path.parts)
    }


def _abstract_types(directory: str) -> list[str]:
    """Interfaces and abstract classes declared under `directory`."""
    pattern = re.compile(r"\binterface\s+(\w+)|\babstract\s+(?:partial\s+)?(?:class|record)\s+(\w+)")
    return [
        first or second
        for text in _sources(directory).values()
        for first, second in pattern.findall(text)
    ]


_SERVICE = Path("Resumes/ResumeService.cs")


def test_gate_summary_of_a_file() -> None:
    _assert_passes("summary of a file")


def test_design_reading_is_passed_in() -> None:
    text = _source(_SERVICE)
    assert "ReadTextFile" not in text, "the service reads the file itself"
    assert not re.search(r"\bFile\s*\.\s*Read|\bStreamReader\b", text), "the service reads the file itself"


def test_design_grading_is_used_directly() -> None:
    assert re.search(r"\bGradeOf\s*\(", _source(_SERVICE)), "the grading rules are the decision"
