from shop.checkout import Cart


def test_cart() -> None:
    assert Cart(total=10.0).total == 10.0
