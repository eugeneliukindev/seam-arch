package shop;

import java.time.Instant;

/** A discount a customer can redeem until it expires. */
public record Coupon(String code, int percent, Instant expires) {
}
