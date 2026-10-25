"""Coupons and the book that keeps them."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class Coupon:
    """A discount a customer can redeem until it expires."""

    code: str
    percent: int
    expires: datetime


class CouponBook:
    """The coupons the shop has issued."""

    def __init__(self) -> None:
        self._coupons: dict[str, Coupon] = {}

    def add(self, coupon: Coupon) -> None:
        """Issue `coupon`."""
        self._coupons[coupon.code] = coupon
