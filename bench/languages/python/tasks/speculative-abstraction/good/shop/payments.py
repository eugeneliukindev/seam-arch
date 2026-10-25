"""Paying for orders."""

from __future__ import annotations

from shop.orders import Order
from shop.stripe_client import StripeClient

CENTS_PER_UNIT = 100


def charge(order: Order, *, card_token: str, client: StripeClient) -> str:
    """Charge `order` to the card behind `card_token` and return the charge id."""
    return client.create_charge(
        amount_cents=int(order.total * CENTS_PER_UNIT), currency=order.currency, source=card_token
    )
