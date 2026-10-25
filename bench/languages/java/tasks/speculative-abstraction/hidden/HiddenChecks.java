import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import shop.Order;
import shop.Payments;
import shop.StripeClient;

public final class HiddenChecks {
    public static void main(String[] args) {
        List<String> charges = new ArrayList<>();
        StripeClient stripe = new StripeClient() {
            @Override
            public String createCharge(long amountCents, String currency, String source) {
                // Stripe itself takes the code in lower case; the case is not the point of the task
                charges.add(amountCents + " " + currency.toUpperCase() + " " + source);
                return "ch_1";
            }
        };
        switch (args[0]) {
            case "cents" -> {
                String id = Payments.charge(new Order(1, new BigDecimal("9.99"), "EUR"), "tok_1", stripe);
                expect(charges.equals(List.of("999 EUR tok_1")), "charges " + charges);
                expect("ch_1".equals(id), "charge id " + id);
            }
            default -> throw new IllegalArgumentException(args[0]);
        }
    }

    private static void expect(boolean passed, String message) {
        if (!passed) {
            throw new AssertionError(message);
        }
    }
}
