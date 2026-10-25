package shop;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

/** The coupons the shop has issued. */
public final class CouponBook {
    private final Map<String, Coupon> coupons = new HashMap<>();

    /** Issue {@code coupon}. */
    public void add(Coupon coupon) {
        coupons.put(coupon.code(), coupon);
    }

    /** {@code total} lowered by the coupon's percent; {@link CouponExpiredException} once it has expired. */
    public BigDecimal apply(String code, BigDecimal total) {
        Coupon coupon = coupons.get(code);
        if (!Instant.now().isBefore(coupon.expires())) {
            throw new CouponExpiredException(code);
        }
        return total.multiply(BigDecimal.valueOf(100 - coupon.percent())).movePointLeft(2);
    }
}
