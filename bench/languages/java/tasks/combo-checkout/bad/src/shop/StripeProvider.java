package shop;

/** Payment through Stripe. */
public final class StripeProvider implements PaymentProvider {
    private final StripeClient client;

    public StripeProvider(StripeClient client) {
        this.client = client;
    }

    @Override
    public String charge(long cents, String token) {
        return client.createCharge(cents, "EUR", token);
    }
}
