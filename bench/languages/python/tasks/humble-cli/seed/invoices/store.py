"""Invoices and where they are kept."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True, kw_only=True)
class Invoice:
    """One invoice sent to a customer."""

    number: str
    due: date
    paid: bool
    amount: float


class InvoiceStore(ABC):
    """Every invoice we have sent."""

    @abstractmethod
    def all(self) -> Sequence[Invoice]:
        """All invoices, in the order they were sent."""
