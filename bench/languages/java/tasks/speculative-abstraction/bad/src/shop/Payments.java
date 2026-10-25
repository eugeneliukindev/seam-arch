package shop;

/** Paying for orders. */
public final class Payments {
    private Payments() {
    }

    /** Charge {@code order} to the card behind {@code cardToken} and return the charge id. */
    public static String charge(Order order, String cardToken, StripeClient client) {
        return client.createCharge(order.total().movePointRight(2).longValueExact(), order.currency(), cardToken);
    }
}
