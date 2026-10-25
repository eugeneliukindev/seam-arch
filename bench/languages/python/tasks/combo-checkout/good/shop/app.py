"""Builds the checkout the site uses."""

from __future__ import annotations

from datetime import UTC, datetime

from shop.checkout import Checkout
from shop.coupons import CouponBook
from shop.stripe_client import StripeClient


def build_checkout(client: StripeClient) -> Checkout:
    """A checkout with an empty coupon book, charging through `client`."""
    return Checkout(coupons=CouponBook(now=lambda: datetime.now(UTC)), client=client)
