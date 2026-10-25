use std::time::{Duration, SystemTime};

use shop::app::build_book;
use shop::coupons::Coupon;

#[test]
fn valid_coupon_lowers_the_total() {
    let mut book = build_book();
    // 2100-01-01
    let expires = SystemTime::UNIX_EPOCH + Duration::from_secs(4_102_444_800);
    book.add(Coupon { code: "A".into(), percent: 10, expires });
    assert_eq!(book.apply("A", 10_000).unwrap(), 9_000);
}
