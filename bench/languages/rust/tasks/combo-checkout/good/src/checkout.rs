//! Taking the customer's money.

use crate::coupons::{CouponBook, CouponError};
use crate::stripe_client::StripeClient;

/// VAT in percent by country; a country not listed pays none.
const VAT_PERCENT: [(&str, u64); 3] = [("GB", 20), ("DE", 19), ("NL", 21)];

/// What the customer is buying.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Cart {
    pub total_cents: u64,
}

/// Discounts, taxes and charges a cart.
pub struct Checkout {
    pub coupons: CouponBook,
    pub(crate) client: Box<dyn StripeClient>,
}

impl Checkout {
    /// Charge the cart after its coupon and VAT; the charge id.
    pub fn pay(&self, cart: &Cart, code: &str, country: &str, card_token: &str) -> Result<String, CouponError> {
        let net = self.coupons.discounted(code, cart.total_cents)?;
        let vat = VAT_PERCENT.iter().find(|(name, _)| *name == country).map_or(0, |(_, percent)| *percent);
        Ok(self.client.create_charge(net * (100 + vat) / 100, "EUR", card_token))
    }
}
