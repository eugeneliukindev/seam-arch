//! Builds the checkout the site uses.

use crate::checkout::{Checkout, StripeProvider};
use crate::coupons::CouponBook;
use crate::stripe_client::StripeClient;

/// A checkout with an empty coupon book, charging through `client`.
pub fn build_checkout(client: Box<dyn StripeClient>) -> Checkout {
    Checkout { coupons: CouponBook::new(), provider: Box::new(StripeProvider { client }) }
}
