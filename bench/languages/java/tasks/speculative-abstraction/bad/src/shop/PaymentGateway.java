package shop;

/** Takes payments for orders. */
public interface PaymentGateway {
    String charge(Order order, String cardToken);
}
