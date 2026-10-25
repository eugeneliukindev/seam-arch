"""The `invoices` command."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from datetime import date
from typing import TextIO

from invoices.store import InvoiceStore


def main(argv: Sequence[str], store: InvoiceStore, today: date, out: TextIO) -> None:
    """Print the invoices, one per line."""
    parser = argparse.ArgumentParser(prog="invoices")
    parser.parse_args(argv)
    for invoice in store.all():
        status = "paid" if invoice.paid else "open"
        print(f"{invoice.number} due {invoice.due} {invoice.amount:.2f} {status}", file=out)
