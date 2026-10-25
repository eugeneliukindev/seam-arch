import io
from datetime import date

from invoices.cli import main
from invoices.store import Invoice, InvoiceStore


class Store(InvoiceStore):
    def all(self) -> list[Invoice]:
        return [
            Invoice(number="A-1", due=date(2026, 1, 10), paid=True, amount=50.0),
            Invoice(number="A-2", due=date(2026, 2, 10), paid=False, amount=75.5),
        ]


def test_lists_every_invoice() -> None:
    out = io.StringIO()
    main([], Store(), date(2026, 3, 1), out)
    assert out.getvalue().splitlines() == [
        "A-1 due 2026-01-10 50.00 paid",
        "A-2 due 2026-02-10 75.50 open",
    ]
