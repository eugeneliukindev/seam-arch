"""Hidden checks for coupon-expiry: expiry is enforced, and the moment it compares against comes from outside."""

import ast
from datetime import UTC, datetime
from pathlib import Path

import pytest

from shop import coupons
from shop.app import build_book


def _book_with(expires: datetime):
    book = build_book()
    book.add(coupons.Coupon(code="A", percent=10, expires=expires))
    return book


def test_gate_valid_coupon_lowers_the_total() -> None:
    assert _book_with(datetime(2100, 1, 1, tzinfo=UTC)).apply("A", 100.0) == pytest.approx(90.0)


def test_gate_expired_coupon_is_refused() -> None:
    with pytest.raises(coupons.CouponExpiredError):
        _book_with(datetime(2000, 1, 1, tzinfo=UTC)).apply("A", 100.0)


_CLOCK_CALLS = {"now", "utcnow", "today", "time", "monotonic"}


def test_design_coupons_never_read_the_clock_themselves() -> None:
    tree = ast.parse(Path("shop/coupons.py").read_text(encoding="utf-8"))
    calls = {ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)}
    found = sorted(c for c in calls if c.split(".")[-1] in _CLOCK_CALLS)
    assert not found, f"shop/coupons.py reads the clock itself: {found}"
