import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import shop.App;
import shop.Cart;
import shop.Checkout;
import shop.Coupon;
import shop.StripeClient;

public final class HiddenChecks {
    public static void main(String[] args) throws Exception {
        List<Long> charges = new ArrayList<>();
        StripeClient stripe = new StripeClient() {
            @Override
            public String createCharge(long amountCents, String currency, String source) {
                charges.add(amountCents);
                return "ch_1";
            }
        };
        Checkout checkout = App.buildCheckout(stripe);
        Cart cart = new Cart(new BigDecimal("100.00"));
        switch (args[0]) {
            case "valid" -> {
                issue(checkout, new Coupon("TEN", 10, Instant.parse("2100-01-01T00:00:00Z")));
                String id = checkout.pay(cart, "TEN", "GB", "tok");
                expect("ch_1".equals(id), "charge id " + id);
                expect(charges.equals(List.of(10800L)), "charges " + charges);
            }
            case "expired" -> {
                issue(checkout, new Coupon("TEN", 10, Instant.parse("2000-01-01T00:00:00Z")));
                try {
                    checkout.pay(cart, "TEN", "DE", "tok");
                    throw new AssertionError("an expired coupon was accepted");
                } catch (RuntimeException refused) {
                    String said = (refused.getClass().getSimpleName() + " " + refused.getMessage()).toLowerCase();
                    expect(said.contains("expir") || said.contains("ten"), "refused with " + refused);
                }
                expect(charges.isEmpty(), "charges " + charges);
            }
            default -> throw new IllegalArgumentException(args[0]);
        }
    }

    /** Issue {@code coupon} in whatever coupon book the checkout holds. */
    private static void issue(Checkout checkout, Coupon coupon) throws Exception {
        for (Class<?> type = checkout.getClass(); type != null; type = type.getSuperclass()) {
            for (Field field : type.getDeclaredFields()) {
                field.setAccessible(true);
                Object value = field.get(checkout);
                if (value == null) {
                    continue;
                }
                for (Method method : value.getClass().getMethods()) {
                    if (method.getName().equals("add") && List.of(method.getParameterTypes()).equals(List.of(Coupon.class))) {
                        method.setAccessible(true);
                        method.invoke(value, coupon);
                        return;
                    }
                }
            }
        }
        throw new AssertionError("no coupon book with add(Coupon) in the checkout");
    }

    private static void expect(boolean passed, String message) {
        if (!passed) {
            throw new AssertionError(message);
        }
    }
}
