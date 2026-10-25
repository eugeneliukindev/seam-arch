"""Hidden checks for humble-cli: --overdue lists the late invoices, decided outside the printing command."""

import re
import subprocess
from pathlib import Path

import pytest

HIDDEN = Path(__file__).parent
CLI = Path("src/invoices/Cli.java")


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


def _check(build: Path, *arguments: str) -> None:
    ran = subprocess.run(
        ["java", "-cp", str(build), "HiddenChecks", *arguments], capture_output=True, text=True, timeout=60, check=False
    )
    assert ran.returncode == 0, ran.stdout + ran.stderr


def test_gate_overdue_lists_late_invoices_oldest_first(build: Path) -> None:
    _check(build, "overdue")


def test_gate_plain_listing_still_lists_everything(build: Path) -> None:
    _check(build, "plain")


_DUE = r"\bdue\b(?:\s*\(\s*\))?"
# comparing a due date, or counting the days from it
_DATE_ARITHMETIC = (
    rf"{_DUE}\s*\.\s*(?:isBefore|isAfter|isEqual|compareTo|until|toEpochDay|plus\w*|minus\w*)\s*\(",
    rf"\.\s*(?:isBefore|isAfter|isEqual|compareTo|until|between)\s*\([^;]*?{_DUE}",
)


def test_design_cli_does_no_date_arithmetic() -> None:
    code = _code(CLI)
    found = [match.group() for pattern in _DATE_ARITHMETIC for match in re.finditer(pattern, code)]
    assert not found, f"the command decides what is overdue itself: {found}"


def _outside_cli(build: Path) -> list[str]:
    """Every named class compiled from src/invoices, but those Cli.java declares."""
    in_cli = set(re.findall(r"\b(?:class|record|enum|interface)\s+(\w+)", _code(CLI)))
    names = []
    for path in sorted((build / "invoices").glob("*.class")):
        if re.search(r"\$\d", path.stem) or path.stem.split("$")[0] in in_cli:
            continue
        names.append(f"invoices.{path.stem}")
    return names


def test_design_a_module_decides_what_is_overdue(build: Path) -> None:
    _check(build, "decides", *_outside_cli(build))
