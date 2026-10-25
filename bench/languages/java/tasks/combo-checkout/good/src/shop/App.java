package shop;

import java.time.Clock;

/** Builds the checkout the site uses. */
public final class App {
    private App() {
    }

    /** A checkout with an empty coupon book, charging through {@code client}. */
    public static Checkout buildCheckout(StripeClient client) {
        return new Checkout(new CouponBook(Clock.systemUTC()), client);
    }
}
