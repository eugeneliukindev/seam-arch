//! Builds the checkout the site uses.

use std::time::SystemTime;

use crate::checkout::Checkout;
use crate::coupons::CouponBook;
use crate::stripe_client::StripeClient;

/// A checkout with an empty coupon book, charging through `client`.
pub fn build_checkout(client: Box<dyn StripeClient>) -> Checkout {
    Checkout { coupons: CouponBook::new(Box::new(SystemTime::now)), client }
}
