package shop;

import java.time.Instant;

final class CouponBookTest {
    public static void main(String[] args) {
        App.buildBook().add(new Coupon("A", 10, Instant.parse("2100-01-01T00:00:00Z")));
        System.out.println("CouponBookTest: ok");
    }
}
