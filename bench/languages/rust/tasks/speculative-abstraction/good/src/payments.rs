//! Paying for orders.

use crate::orders::Order;
use crate::stripe_client::StripeClient;

/// Charge `order` to the card behind `card_token` and return the charge id.
pub fn charge(order: &Order, card_token: &str, client: &dyn StripeClient) -> String {
    client.create_charge(order.total_cents, &order.currency, card_token)
}
