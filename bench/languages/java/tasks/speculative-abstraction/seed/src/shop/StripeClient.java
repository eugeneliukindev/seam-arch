package shop;

/** The client the Stripe SDK would give us; kept small here. */
public class StripeClient {
    /** Charge {@code source} and return the charge id. */
    public String createCharge(long amountCents, String currency, String source) {
        throw new UnsupportedOperationException("configured in production");
    }
}
