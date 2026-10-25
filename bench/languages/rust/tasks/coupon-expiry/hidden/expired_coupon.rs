use std::time::{Duration, SystemTime};

use shop::app::build_book;
use shop::coupons::{Coupon, CouponError};

#[test]
fn expired_coupon_is_refused() {
    let mut book = build_book();
    // 2000-01-01
    let expires = SystemTime::UNIX_EPOCH + Duration::from_secs(946_684_800);
    book.add(Coupon { code: "A".into(), percent: 10, expires });
    let error = book.apply("A", 10_000).unwrap_err();
    assert!(matches!(error, CouponError::Expired { .. }), "not an expiry error: {error:?}");
}
