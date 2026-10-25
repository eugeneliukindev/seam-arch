package invoices;

import java.math.BigDecimal;
import java.time.LocalDate;

/** One invoice sent to a customer. */
public record Invoice(String number, LocalDate due, boolean paid, BigDecimal amount) {
}
