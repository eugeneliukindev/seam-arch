use std::sync::{Arc, Mutex};
use std::time::{Duration, SystemTime};

use shop::app::build_checkout;
use shop::checkout::Cart;
use shop::coupons::Coupon;
use shop::stripe_client::StripeClient;

struct FakeStripe {
    charges: Arc<Mutex<Vec<u64>>>,
}

impl StripeClient for FakeStripe {
    fn create_charge(&self, amount_cents: u64, _currency: &str, _source: &str) -> String {
        self.charges.lock().unwrap().push(amount_cents);
        "ch_1".to_owned()
    }
}

#[test]
fn coupon_vat_and_charge() {
    let charges = Arc::new(Mutex::new(Vec::new()));
    let mut checkout = build_checkout(Box::new(FakeStripe { charges: charges.clone() }));
    // 2100-01-01
    let expires = SystemTime::UNIX_EPOCH + Duration::from_secs(4_102_444_800);
    checkout.coupons.add(Coupon { code: "TEN".into(), percent: 10, expires });
    let paid = checkout.pay(&Cart { total_cents: 10_000 }, "TEN", "GB", "tok");
    assert_eq!(paid.unwrap(), "ch_1");
    assert_eq!(*charges.lock().unwrap(), vec![10_800]);
}
