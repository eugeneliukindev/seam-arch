//! Paying for orders.

use crate::orders::Order;
use crate::stripe_client::StripeClient;

/// Takes payments for orders, so another provider can be added later.
pub trait PaymentGateway {
    /// Charge `order` to the card behind `card_token` and return the charge id.
    fn charge(&self, order: &Order, card_token: &str) -> String;
}

impl<C: StripeClient + ?Sized> PaymentGateway for C {
    fn charge(&self, order: &Order, card_token: &str) -> String {
        self.create_charge(order.total_cents, &order.currency, card_token)
    }
}

/// Charge `order` to the card behind `card_token` and return the charge id.
pub fn charge(order: &Order, card_token: &str, client: &dyn StripeClient) -> String {
    PaymentGateway::charge(client, order, card_token)
}
