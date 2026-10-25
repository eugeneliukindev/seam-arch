package invoices;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;

/** An unpaid invoice past its due date, and by how many days. */
public record Overdue(Invoice invoice, long days) {
    /** The unpaid invoices due before {@code today}, oldest first. */
    public static List<Overdue> of(Collection<Invoice> invoices, LocalDate today) {
        return invoices.stream()
            .filter(invoice -> !invoice.paid() && invoice.due().isBefore(today))
            .sorted(Comparator.comparing(Invoice::due))
            .map(invoice -> new Overdue(invoice, ChronoUnit.DAYS.between(invoice.due(), today)))
            .toList();
    }
}
