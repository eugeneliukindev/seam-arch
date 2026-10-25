package invoices;

import java.io.PrintStream;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

/** The {@code invoices} command. */
public final class Cli {
    private Cli() {
    }

    /** Print the invoices, one per line; with {@code --overdue}, only the late ones. */
    public static void run(String[] args, InvoiceStore store, LocalDate today, PrintStream out) {
        if (List.of(args).equals(List.of("--overdue"))) {
            List<Invoice> sorted = store.all().stream().sorted(Comparator.comparing(Invoice::due)).toList();
            for (Invoice invoice : sorted) {
                if (invoice.paid() || !invoice.due().isBefore(today)) {
                    continue;
                }
                long days = ChronoUnit.DAYS.between(invoice.due(), today);
                out.println(String.format(Locale.ROOT, "%s due %s %.2f %d days overdue",
                    invoice.number(), invoice.due(), invoice.amount(), days));
            }
            return;
        }
        if (args.length > 0) {
            throw new IllegalArgumentException("usage: invoices [--overdue]");
        }
        for (Invoice invoice : store.all()) {
            String status = invoice.paid() ? "paid" : "open";
            out.println(String.format(Locale.ROOT, "%s due %s %.2f %s", invoice.number(), invoice.due(), invoice.amount(), status));
        }
    }
}
