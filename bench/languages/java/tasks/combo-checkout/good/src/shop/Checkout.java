package shop;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Map;

/** Discounts, taxes and charges a cart. */
public final class Checkout {
    private static final Map<String, BigDecimal> VAT_RATES = Map.of(
        "GB", new BigDecimal("0.20"), "DE", new BigDecimal("0.19"), "NL", new BigDecimal("0.21"));

    private final CouponBook coupons;
    private final StripeClient client;

    public Checkout(CouponBook coupons, StripeClient client) {
        this.coupons = coupons;
        this.client = client;
    }

    /** Charge the cart after its coupon and VAT; the charge id. */
    public String pay(Cart cart, String code, String country, String cardToken) {
        BigDecimal net = coupons.discounted(code, cart.total());
        BigDecimal gross = net.multiply(BigDecimal.ONE.add(VAT_RATES.getOrDefault(country, BigDecimal.ZERO)));
        long cents = gross.movePointRight(2).setScale(0, RoundingMode.HALF_UP).longValueExact();
        return client.createCharge(cents, "EUR", cardToken);
    }
}
