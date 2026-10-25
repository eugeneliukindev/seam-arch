//! Coupons and the book that keeps them.

use std::collections::HashMap;
use std::time::SystemTime;

/// A discount a customer can redeem until it expires.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Coupon {
    pub code: String,
    pub percent: u64,
    pub expires: SystemTime,
}

/// Why a coupon cannot be applied.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CouponError {
    /// No coupon was issued under the code.
    Unknown(String),
    /// The coupon's expiry moment has passed.
    Expired(String),
}

/// The coupons the shop has issued.
pub struct CouponBook {
    coupons: HashMap<String, Coupon>,
    now: Box<dyn Fn() -> SystemTime>,
}

impl CouponBook {
    pub fn new(now: Box<dyn Fn() -> SystemTime>) -> Self {
        Self { coupons: HashMap::new(), now }
    }

    /// Issue `coupon`.
    pub fn add(&mut self, coupon: Coupon) {
        self.coupons.insert(coupon.code.clone(), coupon);
    }

    /// `total_cents` lowered by the coupon's percent; an error once it has expired.
    pub fn apply(&self, code: &str, total_cents: u64) -> Result<u64, CouponError> {
        let coupon = self.coupons.get(code).ok_or_else(|| CouponError::Unknown(code.to_owned()))?;
        if (self.now)() >= coupon.expires {
            return Err(CouponError::Expired(code.to_owned()));
        }
        Ok(total_cents * (100 - coupon.percent) / 100)
    }
}
