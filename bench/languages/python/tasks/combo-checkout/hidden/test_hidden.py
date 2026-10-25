"""Hidden checks for combo-checkout: coupon, VAT and charge are right; time comes from outside; VAT is data; Stripe gets no wrapper."""

import ast
from datetime import UTC, datetime
from pathlib import Path

import pytest

from shop.app import build_checkout
from shop.checkout import Cart
from shop.coupons import Coupon
from shop.stripe_client import StripeClient


class FakeStripe(StripeClient):
    def __init__(self) -> None:
        self.charges: list[int] = []

    def create_charge(self, *, amount_cents: int, currency: str, source: str) -> str:
        self.charges.append(amount_cents)
        return "ch_1"


def _checkout_with(expires: datetime):
    stripe = FakeStripe()
    checkout = build_checkout(stripe)
    book = next(v for v in vars(checkout).values() if hasattr(v, "add"))
    book.add(Coupon(code="TEN", percent=10, expires=expires))
    return checkout, stripe


def test_gate_coupon_vat_and_charge() -> None:
    checkout, stripe = _checkout_with(datetime(2100, 1, 1, tzinfo=UTC))
    assert checkout.pay(Cart(total=100.0), "TEN", "GB", "tok") == "ch_1"
    assert stripe.charges == [10800]


def test_gate_expired_coupon_is_refused() -> None:
    checkout, stripe = _checkout_with(datetime(2000, 1, 1, tzinfo=UTC))
    with pytest.raises(Exception, match=r"(?i)TEN|expir"):  # noqa: PT011
        checkout.pay(Cart(total=100.0), "TEN", "DE", "tok")
    assert stripe.charges == []


_CLOCK_CALLS = {"now", "utcnow", "today", "time", "monotonic"}


def _sources() -> dict[str, ast.Module]:
    return {p.name: ast.parse(p.read_text(encoding="utf-8")) for p in Path("shop").glob("*.py") if p.name != "app.py"}


def test_design_time_comes_from_outside() -> None:
    found = sorted(
        f"{name}: {ast.unparse(n.func)}" for name, tree in _sources().items() for n in ast.walk(tree)
        if isinstance(n, ast.Call) and ast.unparse(n.func).split(".")[-1] in _CLOCK_CALLS
    )
    assert not found, f"business code reads the clock itself: {found}"


def test_design_no_type_for_vat_or_payment() -> None:
    extra = []
    for name, tree in _sources().items():
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = {ast.unparse(b).split(".")[-1].split("[")[0] for b in node.bases}
                abstract = bool(bases & {"ABC", "Protocol"})
                named = any(word in node.name.lower() for word in ("vat", "tax", "payment", "provider", "gateway", "processor"))
                clock = any(word in node.name.lower() for word in ("clock", "time"))
                if (abstract and not clock) or named:
                    extra.append(f"{name}: {node.name}")
    assert not extra, f"types for what is data or a single client: {extra}"
