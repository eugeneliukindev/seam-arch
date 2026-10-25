package shop;

import java.math.BigDecimal;

/** What the customer is buying, in euros. */
public record Cart(BigDecimal total) {
}
