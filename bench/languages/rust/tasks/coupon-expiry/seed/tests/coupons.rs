use std::time::{Duration, SystemTime};

use shop::app::build_book;
use shop::coupons::Coupon;

#[test]
fn add() {
    // 2100-01-01
    let expires = SystemTime::UNIX_EPOCH + Duration::from_secs(4_102_444_800);
    build_book().add(Coupon { code: "A".into(), percent: 10, expires });
}
