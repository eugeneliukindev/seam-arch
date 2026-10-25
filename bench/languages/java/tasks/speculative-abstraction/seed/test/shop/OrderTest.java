package shop;

import java.math.BigDecimal;

final class OrderTest {
    public static void main(String[] args) {
        check(new Order(1, new BigDecimal("9.99"), "EUR").total().equals(new BigDecimal("9.99")), "order total");
        System.out.println("OrderTest: ok");
    }

    private static void check(boolean passed, String name) {
        if (!passed) {
            throw new AssertionError(name);
        }
    }
}
