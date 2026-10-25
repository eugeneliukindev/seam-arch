"""Coupons the shop has issued."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


class CouponExpiredError(Exception):
    """The coupon's expiry moment has passed."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Coupon:
    """A discount a customer can redeem until it expires."""

    code: str
    percent: int
    expires: datetime
    """An aware moment in UTC."""


class CouponBook:
    """The coupons the shop has issued."""

    def __init__(self) -> None:
        self._coupons: dict[str, Coupon] = {}

    def add(self, coupon: Coupon) -> None:
        """Issue `coupon`."""
        self._coupons[coupon.code] = coupon

    def discounted(self, code: str, total: float) -> float:
        """`total` lowered by the coupon; `CouponExpiredError` once it has expired."""
        coupon = self._coupons[code]
        if datetime.now(UTC) >= coupon.expires:
            raise CouponExpiredError(code)
        return total * (1 - coupon.percent / 100)
