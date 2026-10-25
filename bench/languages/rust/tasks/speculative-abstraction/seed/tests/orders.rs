use shop::orders::Order;

#[test]
fn order() {
    let order = Order { id: 1, total_cents: 999, currency: "EUR".into() };
    assert_eq!(order.total_cents, 999);
}
