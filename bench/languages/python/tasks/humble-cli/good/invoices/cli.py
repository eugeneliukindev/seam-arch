"""The `invoices` command."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from datetime import date
from typing import TextIO

from invoices.overdue import overdue
from invoices.store import InvoiceStore


def main(argv: Sequence[str], store: InvoiceStore, today: date, out: TextIO) -> None:
    """Print the invoices, one per line; with `--overdue`, only the late ones."""
    parser = argparse.ArgumentParser(prog="invoices")
    parser.add_argument("--overdue", action="store_true", help="only unpaid invoices past due")
    arguments = parser.parse_args(argv)
    if arguments.overdue:
        for late in overdue(store.all(), today):
            invoice = late.invoice
            line = f"{invoice.number} due {invoice.due} {invoice.amount:.2f}"
            print(f"{line} {late.days} days overdue", file=out)
        return
    for invoice in store.all():
        status = "paid" if invoice.paid else "open"
        print(f"{invoice.number} due {invoice.due} {invoice.amount:.2f} {status}", file=out)
