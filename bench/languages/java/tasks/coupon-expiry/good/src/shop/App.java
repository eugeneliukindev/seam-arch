package shop;

import java.time.Clock;

/** Builds the coupon book the till uses. */
public final class App {
    private App() {
    }

    /** A ready, empty coupon book. */
    public static CouponBook buildBook() {
        return new CouponBook(Clock.systemUTC());
    }
}
