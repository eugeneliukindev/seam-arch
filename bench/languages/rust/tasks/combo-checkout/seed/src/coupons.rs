//! Coupons the shop has issued.

use std::collections::HashMap;
use std::time::SystemTime;

/// A discount a customer can redeem until it expires.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Coupon {
    pub code: String,
    pub percent: u64,
    pub expires: SystemTime,
}

/// The coupons the shop has issued.
#[derive(Debug, Default)]
pub struct CouponBook {
    coupons: HashMap<String, Coupon>,
}

impl CouponBook {
    pub fn new() -> Self {
        Self::default()
    }

    /// Issue `coupon`.
    pub fn add(&mut self, coupon: Coupon) {
        self.coupons.insert(coupon.code.clone(), coupon);
    }
}
