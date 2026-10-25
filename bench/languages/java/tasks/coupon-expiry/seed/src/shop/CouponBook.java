package shop;

import java.util.HashMap;
import java.util.Map;

/** The coupons the shop has issued. */
public final class CouponBook {
    private final Map<String, Coupon> coupons = new HashMap<>();

    /** Issue {@code coupon}. */
    public void add(Coupon coupon) {
        coupons.put(coupon.code(), coupon);
    }
}
