use shop::checkout::Cart;

#[test]
fn cart() {
    assert_eq!(Cart { total_cents: 1000 }.total_cents, 1000);
}
