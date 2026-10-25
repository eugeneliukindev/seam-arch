//! Builds the coupon book the till uses.

use std::time::SystemTime;

use crate::coupons::CouponBook;

/// A ready, empty coupon book, reading the system clock.
pub fn build_book() -> CouponBook {
    CouponBook::new(Box::new(SystemTime::now))
}
