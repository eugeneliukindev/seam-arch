//! The client the Stripe SDK would give us; kept small here.

/// Talks to Stripe.
pub trait StripeClient {
    /// Charge `source` and return the charge id.
    fn create_charge(&self, amount_cents: u64, currency: &str, source: &str) -> String;
}
