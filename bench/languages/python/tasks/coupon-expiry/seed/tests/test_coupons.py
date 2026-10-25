from datetime import UTC, datetime

from shop.app import build_book
from shop.coupons import Coupon


def test_add() -> None:
    build_book().add(Coupon(code="A", percent=10, expires=datetime(2100, 1, 1, tzinfo=UTC)))
