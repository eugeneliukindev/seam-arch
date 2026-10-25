"""Taking the customer's money."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Cart:
    """What the customer is buying, in euros."""

    total: float
