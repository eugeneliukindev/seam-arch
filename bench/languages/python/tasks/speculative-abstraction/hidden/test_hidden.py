"""Hidden checks for speculative-abstraction: Stripe works, and no abstract type is added for one implementation."""

import ast
from decimal import Decimal
from pathlib import Path

from shop.orders import Order
from shop.stripe_client import StripeClient


class FakeStripe(StripeClient):
    def __init__(self) -> None:
        self.charges: list[tuple[int, str, str]] = []

    def create_charge(self, *, amount_cents: int, currency: str, source: str) -> str:
        # Stripe itself takes the code in lower case; the case is not the point of the task
        self.charges.append((amount_cents, currency.upper(), source))
        return "ch_1"


def test_gate_charges_in_cents() -> None:
    from shop.payments import charge

    stripe = FakeStripe()
    charge(Order(id=1, total=Decimal("9.99"), currency="EUR"), card_token="tok_1", client=stripe)
    assert stripe.charges == [(999, "EUR", "tok_1")]


def _abstract_types() -> list[str]:
    found = []
    for path in Path("shop").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ClassDef):
                bases = {ast.unparse(base).split(".")[-1].split("[")[0] for base in node.bases}
                abstract = any(
                    "abstractmethod" in ast.unparse(decorator)
                    for item in node.body if isinstance(item, ast.FunctionDef)
                    for decorator in item.decorator_list
                )
                if bases & {"ABC", "Protocol"} or abstract:
                    found.append(node.name)
    return found


def test_design_no_abstract_type_for_one_implementation() -> None:
    assert not _abstract_types(), f"abstract types under a single implementation: {_abstract_types()}"
