"""Builds the coupon book the till uses."""

from __future__ import annotations

from shop.coupons import CouponBook


def build_book() -> CouponBook:
    """A ready, empty coupon book."""
    return CouponBook()
