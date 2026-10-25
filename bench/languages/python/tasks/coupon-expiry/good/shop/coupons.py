"""Coupons and the book that keeps them."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime


class CouponExpiredError(Exception):
    """The coupon's expiry moment has passed."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Coupon:
    """A discount a customer can redeem until it expires."""

    code: str
    percent: int
    expires: datetime


class CouponBook:
    """The coupons the shop has issued."""

    def __init__(self, *, now: Callable[[], datetime]) -> None:
        self._coupons: dict[str, Coupon] = {}
        self._now = now

    def add(self, coupon: Coupon) -> None:
        """Issue `coupon`."""
        self._coupons[coupon.code] = coupon

    def apply(self, code: str, total: float) -> float:
        """`total` lowered by the coupon's percent; `CouponExpiredError` once it has expired."""
        coupon = self._coupons[code]
        if self._now() >= coupon.expires:
            raise CouponExpiredError(code)
        return total * (1 - coupon.percent / 100)
