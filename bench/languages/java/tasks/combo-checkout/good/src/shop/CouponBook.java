package shop;

import java.math.BigDecimal;
import java.time.Clock;
import java.util.HashMap;
import java.util.Map;

/** The coupons the shop has issued. */
public final class CouponBook {
    private final Map<String, Coupon> coupons = new HashMap<>();
    private final Clock clock;

    public CouponBook(Clock clock) {
        this.clock = clock;
    }

    /** Issue {@code coupon}. */
    public void add(Coupon coupon) {
        coupons.put(coupon.code(), coupon);
    }

    /** {@code total} lowered by the coupon; {@link CouponExpiredException} once it has expired. */
    public BigDecimal discounted(String code, BigDecimal total) {
        Coupon coupon = coupons.get(code);
        if (!clock.instant().isBefore(coupon.expires())) {
            throw new CouponExpiredException(code);
        }
        return total.multiply(BigDecimal.valueOf(100 - coupon.percent())).movePointLeft(2);
    }
}
