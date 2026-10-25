//! Builds the coupon book the till uses.

use crate::coupons::CouponBook;

/// A ready, empty coupon book.
pub fn build_book() -> CouponBook {
    CouponBook::new()
}
