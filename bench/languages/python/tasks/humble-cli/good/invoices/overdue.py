"""Which invoices are overdue, and by how long."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from invoices.store import Invoice


@dataclass(frozen=True, slots=True, kw_only=True)
class Overdue:
    """An unpaid invoice past its due date."""

    invoice: Invoice
    days: int


def overdue(invoices: Iterable[Invoice], today: date) -> list[Overdue]:
    """The unpaid invoices due before `today`, oldest first."""
    late = sorted((i for i in invoices if not i.paid and i.due < today), key=lambda i: i.due)
    return [Overdue(invoice=i, days=(today - i.due).days) for i in late]
