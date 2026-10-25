"""Hidden checks for humble-cli: --overdue lists the late invoices, decided outside the printing command."""

import re
import subprocess
from functools import cache
from pathlib import Path

_CHECK = Path(__file__).parent / "Check"
_COMMAND = Path("Invoices/Cli.cs")


def _source(path: Path) -> str:
    """C# source without its comments."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


@cache
def _check_output() -> str:
    """What the check program prints: one `PASS <scenario>` or `FAIL <scenario>: <why>` per line."""
    # the types the command file declares are part of the command, never what decides
    command_types = re.findall(r"\b(?:class|record|struct|interface)\s+(\w+)", _source(_COMMAND))
    completed = subprocess.run(
        ["dotnet", "run", "--project", str(_CHECK), "--", *command_types], capture_output=True, text=True, check=False
    )
    return completed.stdout + completed.stderr


def _assert_passes(scenario: str) -> None:
    assert f"PASS {scenario}" in _check_output().splitlines(), _check_output()


def test_gate_overdue_lists_late_invoices_oldest_first() -> None:
    _assert_passes("overdue lists late invoices oldest first")


def test_gate_plain_listing_still_lists_everything() -> None:
    _assert_passes("plain listing still lists everything")


def test_design_cli_does_no_date_arithmetic() -> None:
    # `Due` compared, added to or subtracted from; `=>` and `->` are not comparisons
    operator = r"(?:(?<![=\-])[<>]=?|[=!]=|-(?!>)|\+)"
    pattern = rf"\bDue\b(?:\s*\.\s*\w+)*\s*{operator}|{operator}\s*[\w.]*\bDue\b|\bDue\s*\.\s*CompareTo\b|\bCompareTo\s*\([^)]*\bDue\b"
    found = [match.group(0) for match in re.finditer(pattern, _source(_COMMAND))]
    assert not found, f"the command decides what is overdue itself: {found}"


def test_design_a_type_outside_the_command_decides_what_is_overdue() -> None:
    _assert_passes("a type outside the command returns the overdue invoices")
