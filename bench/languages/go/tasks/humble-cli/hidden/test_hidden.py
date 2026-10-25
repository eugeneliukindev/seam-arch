"""Hidden checks for humble-cli: -overdue lists the late invoices, decided outside the printing command."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent
# a function the program never calls by a name of its own
_NOT_CANDIDATES = {"init", "main"}


def _go_test(name: str, source: str | None = None) -> None:
    """Run hidden test `name`, from hidden_test.go or from the Go `source` given."""
    target = Path("zz_hidden_checks_test.go")
    if source is None:
        shutil.copy(HIDDEN / "hidden_test.go", target)
    else:
        target.write_text(source, encoding="utf-8")
    try:
        completed = subprocess.run(
            ["go", "test", "-count=1", "-run", f"^{name}$", "./..."], capture_output=True, text=True, check=False
        )
    finally:
        target.unlink()
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _code(path: Path) -> str:
    """The Go source of `path` without its comments and string literals."""
    pattern = r"//[^\n]*|/\*.*?\*/|`[^`]*`|\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'"
    return re.sub(pattern, '""', path.read_text(encoding="utf-8"), flags=re.DOTALL)


def test_gate_overdue_lists_late_invoices_oldest_first() -> None:
    _go_test("TestHiddenOverdueListsLateInvoicesOldestFirst")


def test_gate_plain_listing_still_lists_everything() -> None:
    _go_test("TestHiddenPlainListingStillListsEverything")


def test_design_cli_does_no_date_arithmetic() -> None:
    code = _code(Path("cli.go"))
    due = r"[\w.\[\]]*\bdue\b"
    arithmetic = re.compile(
        rf"{due}\s*\.\s*(?:Before|After|Equal|Compare|Sub|Add|AddDate)\s*\("
        rf"|\.\s*(?:Before|After|Equal|Compare|Sub)\s*\(\s*{due}"
        rf"|\bcmp\.(?:Compare|Less)\s*\([^)]*\bdue\b"
        rf"|{due}[\w.()]*\s*(?:[<>]=?|==|!=)"
        rf"|(?:[<>]=?|==|!=)\s*{due}",
        re.IGNORECASE,
    )
    found = sorted({match.group(0).strip() for match in arithmetic.finditer(code)})
    assert not found, f"the command decides what is overdue itself: {found}"


def _candidates() -> list[str]:
    """Every top-level, non-generic function of the package outside cli.go."""
    names = []
    for path in sorted(Path().glob("*.go")):
        if path.name == "cli.go" or path.name.endswith("_test.go"):
            continue
        names += re.findall(r"^func\s+([A-Za-z_]\w*)\s*\(", _code(path), flags=re.MULTILINE)
    return sorted(set(names) - _NOT_CANDIDATES)


def _package() -> str:
    match = re.search(r"^package\s+(\w+)", _code(Path("cli.go")), flags=re.MULTILINE)
    assert match, "cli.go declares no package"
    return match.group(1)


def test_design_a_function_decides_what_is_overdue() -> None:
    candidates = "".join(f'\t"{name}": {name},\n' for name in _candidates())
    source = (HIDDEN / "overdue_test.go.txt").read_text(encoding="utf-8")
    source = source.replace("package invoices", f"package {_package()}", 1).replace("\t// CANDIDATES\n", candidates)
    _go_test("TestHiddenAFunctionReturnsTheOverdueInvoices", source)
