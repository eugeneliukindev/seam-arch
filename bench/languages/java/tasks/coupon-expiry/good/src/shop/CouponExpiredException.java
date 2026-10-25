package shop;

/** The coupon's expiry moment has passed. */
public final class CouponExpiredException extends RuntimeException {
    public CouponExpiredException(String code) {
        super("coupon " + code + " has expired");
    }
}
