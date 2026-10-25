"""Taking the customer's money."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from shop.coupons import CouponBook
from shop.stripe_client import StripeClient

VAT_RATES = {"GB": 0.20, "DE": 0.19, "NL": 0.21}
CENTS_PER_EURO = 100


class PaymentProvider(ABC):
    """Takes payment."""

    @abstractmethod
    def charge(self, cents: int, token: str) -> str: ...


class StripeProvider(PaymentProvider):
    """Payment through Stripe."""

    def __init__(self, client: StripeClient) -> None:
        self._client = client

    def charge(self, cents: int, token: str) -> str:
        return self._client.create_charge(amount_cents=cents, currency="EUR", source=token)


@dataclass(frozen=True, slots=True, kw_only=True)
class Cart:
    """What the customer is buying, in euros."""

    total: float


class Checkout:
    """Discounts, taxes and charges a cart."""

    def __init__(self, *, coupons: CouponBook, client: StripeClient) -> None:
        self.coupons = coupons
        self._client = client

    def pay(self, cart: Cart, code: str, country: str, card_token: str) -> str:
        """Charge the cart after its coupon and VAT; the charge id."""
        net = self.coupons.discounted(code, cart.total)
        gross = net * (1 + VAT_RATES.get(country, 0.0))
        cents = round(gross * CENTS_PER_EURO)
        return self._client.create_charge(amount_cents=cents, currency="EUR", source=card_token)
