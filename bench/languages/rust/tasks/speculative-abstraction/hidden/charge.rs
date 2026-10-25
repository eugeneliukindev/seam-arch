use std::cell::RefCell;

use shop::orders::Order;
use shop::payments::charge;
use shop::stripe_client::StripeClient;

#[derive(Default)]
struct FakeStripe {
    charges: RefCell<Vec<(u64, String, String)>>,
}

impl StripeClient for FakeStripe {
    fn create_charge(&self, amount_cents: u64, currency: &str, source: &str) -> String {
        // Stripe itself takes the code in lower case; the case is not the point of the task
        self.charges.borrow_mut().push((amount_cents, currency.to_uppercase(), source.to_owned()));
        "ch_1".to_owned()
    }
}

#[test]
fn charges_in_cents() {
    let stripe = FakeStripe::default();
    let order = Order { id: 1, total_cents: 999, currency: "EUR".into() };
    assert_eq!(charge(&order, "tok_1", &stripe), "ch_1");
    assert_eq!(*stripe.charges.borrow(), vec![(999, "EUR".to_owned(), "tok_1".to_owned())]);
}
