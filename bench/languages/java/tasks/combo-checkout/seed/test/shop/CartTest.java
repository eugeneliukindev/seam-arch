package shop;

import java.math.BigDecimal;

final class CartTest {
    public static void main(String[] args) {
        check(new Cart(new BigDecimal("10.00")).total().equals(new BigDecimal("10.00")), "cart total");
        System.out.println("CartTest: ok");
    }

    private static void check(boolean passed, String name) {
        if (!passed) {
            throw new AssertionError(name);
        }
    }
}
