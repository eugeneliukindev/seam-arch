package shop;

import java.math.BigDecimal;

/** An order waiting for payment. */
public record Order(long id, BigDecimal total, String currency) {
}
