"""Hidden checks for humble-cli: --overdue lists the late invoices, decided outside the printing command."""

import re
import shutil
import subprocess
from pathlib import Path

HIDDEN = Path(__file__).parent
CLI = Path("src/cli.rs")
# a path ending in `due`: `due`, `invoice.due`, `late.invoice.due`
_DUE = r"(?:\w+\s*\.\s*)*due\b"
# `due` on either side of a comparison or of `-` and `+`; `->` and `=>` are no operators
_DATE_ARITHMETIC = re.compile(
    rf"\b{_DUE}\s*(?:<=?|>=?|==|!=|-(?!>)|\+)"
    rf"|(?:<=?|(?<![-=])>=?|==|!=|-|\+)\s*[&*(]*\s*\b{_DUE}"
)


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
    """The Rust source of `path` without comments or string literals."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", "", text)
    return re.sub(r"\"(?:[^\"\\]|\\.)*\"", '""', text)


def test_gate_overdue_lists_late_invoices_oldest_first() -> None:
    _cargo_test("overdue")


def test_gate_plain_listing_still_lists_everything() -> None:
    _cargo_test("plain_listing")


def test_design_cli_does_no_date_arithmetic() -> None:
    found = [match.group(0).strip() for match in _DATE_ARITHMETIC.finditer(_code(CLI))]
    assert not found, f"the command decides what is overdue itself: {found}"


def test_design_a_module_decides_what_is_overdue() -> None:
    # a function outside the command that takes the day and gives or takes a collection, and the command calls it
    called = _code(CLI)
    deciders = [
        f"{path}: {name}"
        for path in sorted(Path("src").rglob("*.rs")) if path != CLI
        for name, signature in re.findall(r"\bfn\s+(\w+)([^{;]*)", _code(path))
        if re.search(r"\bDate\b", signature) and re.search(r"\bVec\b|\bIterator\b|\[", signature)
        and re.search(rf"\b{name}\s*(?:::\s*<[^>]*>\s*)?\(", called)
    ]
    assert deciders, "no function outside src/cli.rs gives the command the overdue invoices"
