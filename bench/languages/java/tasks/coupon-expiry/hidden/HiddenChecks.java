import java.math.BigDecimal;
import java.time.Instant;
import shop.App;
import shop.Coupon;
import shop.CouponBook;

public final class HiddenChecks {
    public static void main(String[] args) throws Exception {
        CouponBook book = App.buildBook();
        BigDecimal total = new BigDecimal("100.00");
        switch (args[0]) {
            case "valid" -> {
                book.add(new Coupon("A", 10, Instant.parse("2100-01-01T00:00:00Z")));
                BigDecimal paid = book.apply("A", total);
                expect(paid.compareTo(new BigDecimal("90")) == 0, "paid " + paid);
            }
            case "expired" -> {
                book.add(new Coupon("A", 10, Instant.parse("2000-01-01T00:00:00Z")));
                try {
                    book.apply("A", total);
                    throw new AssertionError("an expired coupon was accepted");
                } catch (Exception refused) {
                    expect(refused.getClass().getSimpleName().equals("CouponExpiredException"), "refused with " + refused);
                }
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
