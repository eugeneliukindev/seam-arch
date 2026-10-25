package shop;

/** Takes payment. */
public interface PaymentProvider {
    String charge(long cents, String token);
}
