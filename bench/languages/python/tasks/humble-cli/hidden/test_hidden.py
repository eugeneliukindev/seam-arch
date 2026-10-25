"""Hidden checks for humble-cli: --overdue lists the late invoices, decided outside the printing command."""

import ast
import contextlib
import dataclasses
import importlib
import inspect
import io
import re
from datetime import date
from pathlib import Path

from invoices.cli import main
from invoices.store import Invoice, InvoiceStore

TODAY = date(2026, 10, 1)
INVOICES = [
    Invoice(number="N-3", due=date(2026, 9, 21), paid=False, amount=300.0),
    Invoice(number="N-1", due=date(2026, 7, 3), paid=False, amount=120.0),
    Invoice(number="N-2", due=date(2026, 8, 25), paid=True, amount=80.0),
    Invoice(number="N-4", due=date(2026, 10, 1), paid=False, amount=60.0),
    Invoice(number="N-5", due=date(2026, 11, 15), paid=False, amount=90.0),
    Invoice(number="N-6", due=date(2026, 9, 2), paid=False, amount=45.25),
]
# oldest first, with days overdue
EXPECTED = [("N-1", 90), ("N-6", 29), ("N-3", 10)]


class Store(InvoiceStore):
    def all(self) -> list[Invoice]:
        return list(INVOICES)


def test_gate_overdue_lists_late_invoices_oldest_first() -> None:
    out = io.StringIO()
    main(["--overdue"], Store(), TODAY, out)
    numbers = {invoice.number for invoice in INVOICES}
    lines = [line for line in out.getvalue().splitlines() if set(re.findall(r"N-\d+", line)) & numbers]
    assert [re.findall(r"N-\d+", line)[0] for line in lines] == [number for number, _ in EXPECTED], out.getvalue()
    for line, (_, days) in zip(lines, EXPECTED, strict=True):
        assert re.search(rf"(?<![\d.-]){days}(?![\d.-])", line), f"no {days} days in {line!r}"


def test_gate_plain_listing_still_lists_everything() -> None:
    out = io.StringIO()
    main([], Store(), TODAY, out)
    assert all(invoice.number in out.getvalue() for invoice in INVOICES)


def test_design_cli_does_no_date_arithmetic() -> None:
    tree = ast.parse(Path("invoices/cli.py").read_text(encoding="utf-8"))
    found = [
        ast.unparse(node)
        for node in ast.walk(tree)
        if isinstance(node, ast.Compare | ast.BinOp)
        and any(
            isinstance(name, ast.Attribute) and name.attr == "due" or isinstance(name, ast.Name) and name.id == "due"
            for operand in ([node.left, *node.comparators] if isinstance(node, ast.Compare) else [node.left, node.right])
            for name in ast.walk(operand)
        )
    ]
    assert not found, f"the command decides what is overdue itself: {found}"


def _invoices_in(item: object) -> list[Invoice]:
    if isinstance(item, Invoice):
        return [item]
    if isinstance(item, tuple | list):
        values = list(item)
    elif dataclasses.is_dataclass(item):
        values = [getattr(item, field.name) for field in dataclasses.fields(item)]
    else:
        values = list(getattr(item, "__dict__", {}).values())
    return [value for value in values if isinstance(value, Invoice)]


def _returns_overdue(function: object) -> bool:
    for arguments in ((list(INVOICES), TODAY), (TODAY, list(INVOICES))):
        printed = io.StringIO()
        try:
            with contextlib.redirect_stdout(printed):
                result = list(function(*arguments))  # type: ignore[operator]
        except Exception:  # noqa: BLE001
            continue
        found = [invoice.number for item in result for invoice in _invoices_in(item)]
        if found and sorted(found) == sorted(number for number, _ in EXPECTED) and not printed.getvalue():
            return True
    return False


def test_design_a_module_decides_what_is_overdue() -> None:
    candidates = []
    for path in sorted(Path("invoices").glob("*.py")):
        if path.stem in {"cli", "__init__"}:
            continue
        module = importlib.import_module(f"invoices.{path.stem}")
        candidates += [
            value for value in vars(module).values()
            if inspect.isfunction(value) and value.__module__ == module.__name__
        ]
    assert any(_returns_overdue(function) for function in candidates), "no function outside cli.py returns the overdue invoices"
